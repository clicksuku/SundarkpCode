resource "google_bigquery_dataset" "default" {
  dataset_id                  = var.dataset_id
  friendly_name               = var.dataset_id
  description                 = "This is a Data Engineering Zoomcamp Project by Sundarkp"
  location                    = var.location

  labels = {
    env = "default"
  }
}
