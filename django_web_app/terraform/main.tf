provider "aws" {
  region = "us-west-2"
}

# Logging bucket for S3 access logs
resource "aws_s3_bucket" "log_bucket" {
  bucket = "my-log-bucket"
}

# SNS topic for S3 event notifications
resource "aws_sns_topic" "s3_events" {
  name = "s3-event-topic"
}

# Secure S3 bucket with encryption, logging, and notifications
resource "aws_s3_bucket" "good_example" {
  bucket = "my-secure-bucket"

  logging {
    target_bucket = aws_s3_bucket.log_bucket.bucket
    target_prefix = "log/"
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

# Event notification for secure S3 bucket
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.good_example.id

  topic {
    topic_arn = aws_sns_topic.s3_events.arn
    events    = ["s3:ObjectCreated:*"]
  }
}

# Insecure S3 bucket (intentionally vulnerable)
resource "aws_s3_bucket" "bad_example" {
  bucket = "my-unsecure-bucket"
}

# Insecure security group (intentionally vulnerable)
resource "aws_security_group" "allow_all" {
  description = "Allow HTTP traffic from any source"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP from the internet"
  }
}

# Secure security group
resource "aws_security_group" "restricted" {
  description = "Allow HTTP only from internal network"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
    description = "Allow HTTP from VPC range"
  }
}

