#!/bin/bash

# Azure Web App 시작 스크립트
echo "Starting LG Battery Cost Analysis System..."

# Python 패키지 설치
pip install -r requirements.txt

# Flask 서버 시작
cd visualization
gunicorn --bind=0.0.0.0:8000 --timeout 600 graph_api_server:app
