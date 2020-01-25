///*
output "nginx_ip_address" {
  value = module.aws_instance_nginx.public_ip
}
//*/
output "c2_ip_address" {
  value = module.aws_instance_c2.public_ip
}
