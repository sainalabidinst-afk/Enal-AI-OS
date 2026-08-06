resource "aws_db_instance" "default" {
  allocated_storage    = 20
  engine               = "mysql"
  username             = "admin"
  password             = "MyP@ssw0rd123"
  skip_final_snapshot  = true
  publicly_accessible  = true
}