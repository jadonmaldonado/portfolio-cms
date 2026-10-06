resource "aws_db_subnet_group" "portfolio" {
  name = "${var.project_name}-db-subnets"

  subnet_ids = [
    aws_subnet.private_db_a.id,
    aws_subnet.private_db_b.id
  ]

  tags = {
    Name = "${var.project_name}-db-subnets"
  }
}

resource "aws_db_instance" "portfolio" {
  identifier = "${var.project_name}-db"

  engine         = "postgres"
  engine_version = "16"

  instance_class = "db.t3.micro"

  allocated_storage     = 20
  max_allocated_storage = 20
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = var.db_name
  username = var.db_username
  password = random_password.db.result
  port     = 5432

  db_subnet_group_name = aws_db_subnet_group.portfolio.name

  vpc_security_group_ids = [
    aws_security_group.db.id
  ]

  publicly_accessible = false
  multi_az            = false

  deletion_protection = true

  skip_final_snapshot       = false
  final_snapshot_identifier = "${var.project_name}-final"

  backup_retention_period = 7

  auto_minor_version_upgrade = true

  lifecycle {
    prevent_destroy = true
  }

  tags = {
    Name = "${var.project_name}-db"
  }
}

output "db_endpoint" {
  value = aws_db_instance.portfolio.address
}

output "db_port" {
  value = aws_db_instance.portfolio.port
}