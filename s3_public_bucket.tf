resource "aws_s3_bucket" "bad_example" {
  bucket = "open-bucket"
  acl    = "public-read"
}
