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

db_endpoint = "${db_endpoint}"
db_port = "${db_port}"
aws_region = "${aws_region}"
s3_bucket_name = "${s3_bucket_name}"

client = boto3.client("secretsmanager", region_name=region)
response = client.get_secret_value(SecretId=secret_arn)
secret = json.loads(response["SecretString"])

import shlex

database_url = (
    f"postgresql+psycopg://{secret['username']}:{secret['password']}"
    f"@{db_endpoint}:{db_port}/{secret['dbname']}"
)

with open("/etc/portfolio-cms.env", "w") as f:
    f.write(f"DATABASE_URL={shlex.quote(database_url)}\n")
    f.write(f"AWS_DEFAULT_REGION={shlex.quote(aws_region)}\n")
    f.write(f"S3_BUCKET_NAME={shlex.quote(s3_bucket_name)}\n")
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

sleep 5
echo "===== PORTFOLIO CMS SERVICE STATUS ====="
systemctl status portfolio-cms --no-pager || true

echo "===== PORT 5000 ====="
ss -lntp | grep ':5000' || true

echo "===== LOCAL HTTP TEST ====="
curl -i http://127.0.0.1:5000/ || true