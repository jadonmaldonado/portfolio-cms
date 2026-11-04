data "aws_s3_bucket" "uploads" {
  bucket = var.s3_bucket_name
}