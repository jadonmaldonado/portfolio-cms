#!/bin/bash

set -e

dnf update -y
dnf install -y git python3.11 python3.11-pip

mkdir -p /opt/portfolio-cms
cd /opt

git clone --branch ${github_branch} ${github_repo} portfolio-cms

cd /opt/portfolio-cms/application/cms

python3.11 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install gunicorn boto3

python - <<'PY'
import json
import boto3

secret_arn = "${db_secret_arn}"
region = "${aws_region}"

client = boto3.client("secretsmanager", region_name=region)
response = client.get_secret_value(SecretId=secret_arn)
secret = json.loads(response["SecretString"])

with open("/etc/portfolio-cms.env", "w") as f:
    f.write(
        "DATABASE_URL="
        f"postgresql+psycopg://{secret['username']}:{secret['password']}"
        f"@${db_endpoint}:${db_port}/{secret['dbname']}\n"
    )
    f.write("AWS_DEFAULT_REGION=${aws_region}\n")
    f.write("S3_BUCKET_NAME=${s3_bucket_name}\n")
    f.write("SECRET_KEY=dev-secret-key\n")
PY

chmod 600 /etc/portfolio-cms.env

set -a
source /etc/portfolio-cms.env
set +a

python -c "
from app import app
from extensions import db
from models.project import Project
from models.certification import Certification
from models.site_content import SiteContent
from models.resume import Resume

with app.app_context():
    db.create_all()
"

cat > /etc/systemd/system/portfolio-cms.service <<EOF
[Unit]
Description=Portfolio CMS Flask Application
After=network.target

[Service]
User=root
WorkingDirectory=/opt/portfolio-cms/application/cms
EnvironmentFile=/etc/portfolio-cms.env
ExecStart=/opt/portfolio-cms/application/cms/.venv/bin/gunicorn --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable portfolio-cms
systemctl start portfolio-cms