provider "aws" {
  region = "us-west-2"
}

# Define a secure S3 bucket (negative case)
resource "aws_s3_bucket" "good_example" {
  bucket = "my-secure-bucket"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

# Define an insecure S3 bucket (positive case, vulnerable)
resource "aws_s3_bucket" "bad_example" {
  bucket = "my-unsecure-bucket"
}

# Define an insecure security group (positive case, vulnerable)
resource "aws_security_group" "allow_all" {
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Define a secure security group (negative case, secure)
resource "aws_security_group" "restricted" {
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
}
