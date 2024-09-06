
variable "projectId" {
  description = "Project"
  default     = "<Project ID>"
}


variable "project" {
  description = "Project"
  default     = "<Project Name>"
}

variable "vmname" {
  description = "VM Name"
  default     = "skpolistvm"
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

variable "machinetype" {
  description = "Machine Type"
  #Update the below to your desired location
  default = "e2-standard-8"
}


variable "osimage" {
  description = "OS Image"
  #Update the below to your desired location
  default = "projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20240307b"
}


