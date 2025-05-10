pipeline {
    agent any

    environment {
        DJANGO_DIR = '/home/kali/Django-WebApp/django_web_app'
        DJANGO_PORT = '8000'
    }

    stages {
        stage('Checkout Code') {
            steps {
                sh '''
                    rm -rf Django-WebApp
                    git clone https://github.com/asnaarshad/Django-WebApp.git
                '''
            }
        }

        stage('Set Up Python Environment') {
            steps {
                dir("${env.DJANGO_DIR}") {
                    sh '''
                        
                        pip install -r requirements.txt || true
                        pip install pylint bandit semgrep flake8 || true
                    '''
                }
            }
        }

        stage('Start Django Server') {
            steps {
                dir("${env.DJANGO_DIR}") {
                    sh '''
                        source venv/bin/activate
                        python manage.py migrate
                        nohup python manage.py runserver 0.0.0.0:${DJANGO_PORT} &
                        sleep 10
                        curl -sSf http://localhost:${DJANGO_PORT} > /dev/null || {
                            echo "Django server failed to start"
                            exit 1
                        }
                    '''
                }
            }
        }

        stage('Check Code Lint') {
            steps {
                dir("${env.DJANGO_DIR}") {
                    sh 'pylint . > lint-report.txt || true'
                }
            }
        }

        stage('Flake8 Check') {
            steps {
                dir("${env.DJANGO_DIR}") {
                    sh 'flake8 . > flake8-report.txt || true'
                }
            }
        }

        stage('Check for Secret Keys') {
            steps {
                dir("${env.DJANGO_DIR}") {
                    sh 'grep -r "SECRET_KEY" . > secret-key-check.txt || true'
                }
            }
        }

        stage('Bandit Scan') {
            steps {
                dir("${env.DJANGO_DIR}") {
                    sh 'bandit -r . -f txt -o bandit-report.txt || true'
                }
            }
        }

        stage('Semgrep Scan') {
            steps {
                dir("${env.DJANGO_DIR}") {
                    sh 'semgrep --config "p/python" . > semgrep-report.txt || true'
                }
            }
        }

        stage('Snyk Dependency Scan') {
            steps {
                dir("${env.DJANGO_DIR}") {
                    sh '''
                        snyk auth || true
                        snyk test --file=requirements.txt --severity-threshold=low || true
                        snyk test --file=requirements.txt --json > snyk-report.json || true
                    '''
                }
            }
        }

        stage('DAST - OWASP ZAP Scan') {
            steps {
                sh 'docker run --network="host" -t owasp/zap2docker-stable zap-baseline.py -t http://localhost:8000'
            }
        }

        stage('DAST - SQLMap Scan') {
            steps {
                sh 'sqlmap -u "http://localhost:8000/vulnerable_endpoint/?id=1" --batch'
            }
        }

        stage('Container Security - Trivy') {
            steps {
                dir("${env.DJANGO_DIR}") {
                    sh '''
                        docker build -t django_webapp_scanned .
                        trivy image django_webapp_scanned
                    '''
                }
            }
        }

        stage('Container Security - Docker Bench') {
            steps {
                sh '''
                    git clone https://github.com/docker/docker-bench-security.git || true
                    cd docker-bench-security
                    sh docker-bench-security.sh
                '''
            }
        }

        stage('IaC Security - Conftest') {
            steps {
                sh 'conftest test terraform/ || true'
            }
        }

        stage('IaC Security - Checkov') {
            steps {
                sh 'checkov -d terraform/ || true'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/*.txt, **/*.json', fingerprint: true
        }
    }
}
