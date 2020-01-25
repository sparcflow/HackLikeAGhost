variable "domain" {
  default = "www.customdomain.com"
}
variable "certificateARN"{
  default = "ARN_TO_PROVIDE"
}
variable "adminIP" {
  default = "0.0.0.0/0"
}

variable "nginxContainer" {
  default = "sparcflow/nginx:prod"
}

variable "C2Container" {
  default = "sparcflow/silent:prod"
}

