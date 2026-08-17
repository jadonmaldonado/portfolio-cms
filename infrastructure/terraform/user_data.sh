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
python -m pip install gunicorn

cat > /etc/systemd/system/portfolio-cms.service <<EOF
[Unit]
Description=Portfolio CMS Flask Application
After=network.target

[Service]
User=root
WorkingDirectory=/opt/portfolio-cms/application/cms
Environment="AWS_DEFAULT_REGION=${aws_region}"
Environment="S3_BUCKET_NAME=${s3_bucket_name}"
Environment="SECRET_KEY=dev-secret-key"
ExecStart=/opt/portfolio-cms/application/cms/.venv/bin/gunicorn --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable portfolio-cms
systemctl start portfolio-cms