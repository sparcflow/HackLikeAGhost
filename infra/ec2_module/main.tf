#
# AWS EC2 Instance
#

resource "aws_instance" "basic_ec2" {
  ami           = "ami-0039c41a10b230acb"
  instance_type = "t2.micro"
  tags = {
    Name = var.name
  }
  vpc_security_group_ids      = var.security_groups
  user_data                   = var.user_data
  key_name                    = var.sshkey
  associate_public_ip_address = "true"
  root_block_device {
    volume_size = "25"
  }
}
