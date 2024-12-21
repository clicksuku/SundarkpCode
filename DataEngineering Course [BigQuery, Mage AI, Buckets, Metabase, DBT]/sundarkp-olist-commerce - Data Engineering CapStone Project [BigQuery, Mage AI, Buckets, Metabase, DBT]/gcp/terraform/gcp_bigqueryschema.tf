resource "google_bigquery_dataset" "default" {
  dataset_id                  = "olist"
  friendly_name               = "olist"
  description                 = "This is a Data Engineering Zoomcamp Project by Sundarkp"
  location                    = "US"

  labels = {
    env = "default"
  }
}