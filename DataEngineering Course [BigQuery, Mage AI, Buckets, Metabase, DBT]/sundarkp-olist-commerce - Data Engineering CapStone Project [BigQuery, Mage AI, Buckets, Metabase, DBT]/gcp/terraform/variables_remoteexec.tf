
variable "user" {
  description = "User Name"
  default     = "sundarkp"
}

variable "privatekeypath" {
  description = "Private Key"
  default     = "~/.ssh/google_compute_engine"
}

variable "publickeypath" {
  description = "Public Key"
  default     = "~/.ssh/google_compute_engine.pub"
}