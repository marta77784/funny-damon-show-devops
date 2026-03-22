terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = "us-west-2"
  profile = "marta"
}

resource "aws_s3_bucket" "funny_damon_stats" {
  bucket = "funny-damon-show-stats-tf"

  tags = {
    Name        = "Funny Damon Show Stats"
    Environment = "Production"
    Project     = "funny-damon-show-devops"
  }
}

output "bucket_name" {
  value = aws_s3_bucket.funny_damon_stats.bucket
}
