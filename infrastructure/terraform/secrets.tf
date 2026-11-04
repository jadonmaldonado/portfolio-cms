resource "random_password" "db" {
  length           = 32
  special          = true
  override_special = "!#$%^&*()-_=+[]{}:?"
}

resource "aws_secretsmanager_secret" "db" {
  name                    = "${var.project_name}-db"
  description             = "Database credentials for Portfolio CMS"
  recovery_window_in_days = 0

  tags = {
    Name = "${var.project_name}-db-secret"
  }
}

resource "aws_secretsmanager_secret_version" "db" {
  secret_id = aws_secretsmanager_secret.db.id

  secret_string = jsonencode({
    username = var.db_username
    password = random_password.db.result
    dbname   = var.db_name
  })
}

output "db_secret_arn" {
  value = aws_secretsmanager_secret.db.arn
}