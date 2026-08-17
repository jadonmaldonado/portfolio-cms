variable "aws_region" {
  type    = string
  default = "us-west-1"
}

variable "project_name" {
  type    = string
  default = "portfolio-cms"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "owner" {
  type    = string
  default = "jadonmaldonado"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "s3_bucket_name" {
  type        = string
  description = "Existing S3 bucket used by the portfolio application"
}

variable "github_repo" {
  type    = string
  default = "https://github.com/jadonmaldonado/portfolio-cms.git"
}

variable "github_branch" {
  type    = string
  default = "feature/certifications"
}