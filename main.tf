resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-unsecured-bucket"
  acl    = "public-read"
}
