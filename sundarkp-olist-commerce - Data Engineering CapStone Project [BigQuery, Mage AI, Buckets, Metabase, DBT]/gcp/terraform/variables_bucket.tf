
variable "gcs_bucket_name" {
  description = "OLIST Marketing and Customer"
  #Update the below to a unique bucket name
  default = "skp-olist-gcp"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}