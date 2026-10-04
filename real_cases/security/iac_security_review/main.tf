resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.web.id]
  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y python3
              EOF
}

resource "aws_security_group" "web" {
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "default" {
  username             = "admin"
  password             = "MyP@ssw0rd123"
  skip_final_snapshot  = true
  publicly_accessible  = true
}