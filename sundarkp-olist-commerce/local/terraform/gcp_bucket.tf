resource "google_storage_bucket" "static" {
  name          = var.gcs_bucket_name
  location      = "US"
  storage_class = var.gcs_storage_class

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
}
