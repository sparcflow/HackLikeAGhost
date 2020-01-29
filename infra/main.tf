resource "aws_key_pair" "ssh_key" {
  key_name   = "adminKey"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxsvdQMb/ifGtaR7lYBwpvAa0L1DWGMaia4yGpUq2uN8jUaFDmwuXXApIYC4S0nOp4znFlyV6phk427Nk0J2n5t+MJiFTmATUIZoZhMyBXHKedysOYRUuycDYFI62sr0vDFDMfjdzt63MgJhhIVFKs9Zu8pdisI8R3d7cWf+BkMi0aOGc6j3Pvj/XH+c0IpoV58cmhSUx1BVM9HkRDoyzNzV3H1/Qki1YDVdfrgrL5mAtA94VoYUft7PMYw4mzyLVip9nTIaBfVFJ/ebCjeX8/SYSk+5M3MPBbRGrsF2WQIl986OdxGmOlKXLFQrzTcnzcBZBjsnba3snNY2H2zQ+P"
}

resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}

resource "aws_security_group" "HTTPAny" {
  name        = "NginxInternet"
  description = "HTTP Any rule"
  vpc_id      = aws_default_vpc.default.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "BackendTCP" {
  name        = "BackendTCP"
  description = "Traffic from Nginx to C2"
  vpc_id      = aws_default_vpc.default.id
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = [aws_default_vpc.default.cidr_block]
  }
  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = [aws_default_vpc.default.cidr_block]
  }
}

resource "aws_security_group" "MgmtSG" {
  name        = "mgmtSG"
  description = "Management traffic"
  vpc_id      = aws_default_vpc.default.id
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.adminIP]
  }
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = [var.adminIP]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

module "aws_instance_c2" {
  name            = "C2"
  source          = "./ec2_module"
  sshkey          = aws_key_pair.ssh_key.id
  security_groups = [aws_security_group.BackendTCP.id, aws_security_group.MgmtSG.id]
  user_data       = <<EOF
#!/bin/bash
CONTAINER="${var.C2Container}";
${file("./scripts/silent.sh")}
rm /var/lib/cloud/instances/*/sem/config_scripts_user
EOF
}

module "aws_instance_nginx" {
  name            = "nginx"
  source          = "./ec2_module"
  sshkey          = aws_key_pair.ssh_key.id
  security_groups = [aws_security_group.HTTPAny.id, aws_security_group.BackendTCP.id, aws_security_group.MgmtSG.id]
  user_data       = <<EOF
#!/bin/bash
DOMAIN="${var.domain}";
C2IP="${module.aws_instance_c2.private_ip}";
CONTAINER="${var.nginxContainer}";

sleep 30
${file("./scripts/nginx.sh")}
rm /var/lib/cloud/instances/*/sem/config_scripts_user
EOF
}
