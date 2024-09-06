resource "google_storage_bucket" "static" {
  name          = "skp-olist-gcp"
  location      = "US"
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
}
