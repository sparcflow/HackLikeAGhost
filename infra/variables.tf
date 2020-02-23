variable "adminIP" {
  default = "0.0.0.0/0"
}
variable "C2Container" {
  default = "sparcflow/silent:prod"
}
variable "certificateARN"{
  default = "ARN_TO_PROVIDE"
}
variable "domain" {
  default = "www.customdomain.com"
}
variable "nginxContainer" {
  default = "sparcflow/nginx:prod"
}
variable "sshkey" {
  default = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxsvdQMb/ifGtaR7lYBwpvAa0L1DWGMaia4yGpUq2uN8jUaFDmwuXXApIYC4S0nOp4znFlyV6phk427Nk0J2n5t+MJiFTmATUIZoZhMyBXHKedysOYRUuycDYFI62sr0vDFDMfjdzt63MgJhhIVFKs9Zu8pdisI8R3d7cWf+BkMi0aOGc6j3Pvj/XH+c0IpoV58cmhSUx1BVM9HkRDoyzNzV3H1/Qki1YDVdfrgrL5mAtA94VoYUft7PMYw4mzyLVip9nTIaBfVFJ/ebCjeX8/SYSk+5M3MPBbRGrsF2WQIl986OdxGmOlKXLFQrzTcnzcBZBjsnba3snNY2H2zQ+P"
}
