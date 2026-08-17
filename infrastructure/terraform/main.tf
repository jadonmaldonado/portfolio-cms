locals {
  az_a = "us-west-1a"
  az_b = "us-west-1b"

  public_a_cidr      = "10.0.1.0/24"
  public_b_cidr      = "10.0.2.0/24"
  private_app_a_cidr = "10.0.11.0/24"
  private_app_b_cidr = "10.0.12.0/24"
  private_db_a_cidr  = "10.0.21.0/24"
  private_db_b_cidr  = "10.0.22.0/24"
}

resource "aws_vpc" "portfolio" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_internet_gateway" "portfolio" {
  vpc_id = aws_vpc.portfolio.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.portfolio.id
  cidr_block              = local.public_a_cidr
  availability_zone       = local.az_a
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-a"
    Tier = "public"
  }
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.portfolio.id
  cidr_block              = local.public_b_cidr
  availability_zone       = local.az_b
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-b"
    Tier = "public"
  }
}

resource "aws_subnet" "private_app_a" {
  vpc_id            = aws_vpc.portfolio.id
  cidr_block        = local.private_app_a_cidr
  availability_zone = local.az_a

  tags = {
    Name = "${var.project_name}-app-a"
    Tier = "private-app"
  }
}

resource "aws_subnet" "private_app_b" {
  vpc_id            = aws_vpc.portfolio.id
  cidr_block        = local.private_app_b_cidr
  availability_zone = local.az_b

  tags = {
    Name = "${var.project_name}-app-b"
    Tier = "private-app"
  }
}

resource "aws_subnet" "private_db_a" {
  vpc_id            = aws_vpc.portfolio.id
  cidr_block        = local.private_db_a_cidr
  availability_zone = local.az_a

  tags = {
    Name = "${var.project_name}-db-a"
    Tier = "private-db"
  }
}

resource "aws_subnet" "private_db_b" {
  vpc_id            = aws_vpc.portfolio.id
  cidr_block        = local.private_db_b_cidr
  availability_zone = local.az_b

  tags = {
    Name = "${var.project_name}-db-b"
    Tier = "private-db"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.portfolio.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.portfolio.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

resource "aws_route_table_association" "public_a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "private_app" {
  vpc_id = aws_vpc.portfolio.id

  tags = {
    Name = "${var.project_name}-app-rt"
  }
}

resource "aws_route_table_association" "private_app_a" {
  subnet_id      = aws_subnet.private_app_a.id
  route_table_id = aws_route_table.private_app.id
}

resource "aws_route_table_association" "private_app_b" {
  subnet_id      = aws_subnet.private_app_b.id
  route_table_id = aws_route_table.private_app.id
}

resource "aws_route_table" "private_db" {
  vpc_id = aws_vpc.portfolio.id

  tags = {
    Name = "${var.project_name}-db-rt"
  }
}

resource "aws_route_table_association" "private_db_a" {
  subnet_id      = aws_subnet.private_db_a.id
  route_table_id = aws_route_table.private_db.id
}

resource "aws_route_table_association" "private_db_b" {
  subnet_id      = aws_subnet.private_db_b.id
  route_table_id = aws_route_table.private_db.id
}