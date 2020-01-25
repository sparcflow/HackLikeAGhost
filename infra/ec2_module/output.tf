output "id" {
  value = "${aws_instance.basic_ec2.id}"
}
output "public_ip" {
  value = "${aws_instance.basic_ec2.public_ip}"
}
output "private_ip" {
  value = "${aws_instance.basic_ec2.private_ip}"
}
