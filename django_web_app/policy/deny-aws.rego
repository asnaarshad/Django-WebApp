package main

deny[msg] {
  input.resource.provider == "aws"
  msg = "AWS provider is not allowed"
}

