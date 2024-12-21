
variable "projectId" {
  description = "Project ID"
  default     = "<Project ID>"
}

variable "project" {
  description = "Project"
  default     = "<PROJECT_NAME>"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default = "US"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default = "us-west4"
}

variable "zone" {
  description = "Zone"
  #Update the below to your desired region
  default = "us-west4-b"
}

variable "gcs_bucket_name" {
  description = "OLIST Marketing and Customer"
  #Update the below to a unique bucket name
  default = "skp-olist-gcp"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "dataset_id" {
  description = "Dataset ID"
  default     = "olist"
}

variable "gcpkey" {
  sensitive   = true
  description = "Google Cloud service account credentials"
}