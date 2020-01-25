resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}
resource "aws_lb_target_group" "tg_name" {
  name     = var.name
  port     = var.port
  protocol = "HTTP"
  vpc_id   = aws_default_vpc.default.id
}

resource "aws_lb_target_group_attachment" "silent_tg_attachment" {
  target_group_arn = aws_lb_target_group.tg_name.arn
  target_id        = var.instanceID
  port             = var.port
}

resource "aws_lb_listener_rule" "static" {
  listener_arn = var.albListenerID
  priority     = var.priority

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg_name.arn
  }

  condition {
    path_pattern {
      values = var.patterns
    }
  }

  condition {
    host_header {
      values = var.domain
    }
  }
}