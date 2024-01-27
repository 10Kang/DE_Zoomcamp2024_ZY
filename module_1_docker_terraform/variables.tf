
variable "credentials" {
  description = "My Credentials"
  default     = "gcp_terraform.json"
  #ex: if you have a directory where this file is called keys with your service account json file
  #saved there as my-creds.json you could use default = "./keys/my-creds.json"
}

variable "project" {
  description = "Project"
  default     = "de-zoomcamp-412301"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "zy_zoomcamp_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "ze-zoomcamp-zy"
}


variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "Standard"
}

variable "location" {
  description = "Project Location"
  default     = "asia-southeast1"
}
