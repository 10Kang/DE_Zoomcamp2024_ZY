
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
  default     = "malaysian_coffee_chain"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "malaysian_coffee_chain"
}


variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "Standard"
}

variable "location" {
  description = "Project Location"
  default     = "asia-southeast1"
}

variable "storage_class" {
  description = "Storage class of bucket"
  default     = "STANDARD"
}

variable "ubuntu_2004_sku" {
  type        = string
  description = "SKU for Ubuntu 20.04 LTS"
  default     = "ubuntu-os-cloud/ubuntu-2004-lts"
}