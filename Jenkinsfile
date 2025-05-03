pipeline {
    agent any
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install pylint bandit flake8'
            }
        }
        stage('Check Code Lint') {
            steps {
                sh 'pylint webapp/ > lint-report.txt || true'
            }
        }
        stage('Check for Secret Keys') {
            steps {
                sh 'grep -r "SECRET_KEY" webapp/ > secret-key-check.txt || true'
            }
        }
        stage('Bandit Scan') {
            steps {
                sh 'bandit -r webapp/ -f txt -o bandit-report.txt || true'
            }
        }
        stage('Flake8 Lint') {
            steps {
                sh 'flake8 webapp/ > flake8-report.txt || true'
            }
        }
        stage('Dependency Check') {
            steps {
                sh '''
                ./dependency-check/bin/dependency-check.sh --project "Django-WebApp" --scan . --format HTML --out dependency-report
                '''
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: '*.txt', fingerprint: true
        }
    }
}
