#!/bin/bash

echo "🔨 Docker 이미지를 다시 빌드합니다..."

# 서비스 중지
echo "📦 기존 서비스를 중지합니다..."
docker-compose down

# 이미지 다시 빌드
echo "🔨 FastAPI 이미지를 다시 빌드합니다..."
docker-compose build --no-cache

# 서비스 시작
echo "🚀 서비스를 시작합니다..."
docker-compose up -d

echo ""
echo "✅ 이미지 재빌드가 완료되었습니다!"
echo "🌐 API 문서: http://localhost:8000"
echo ""
echo "📋 로그를 확인하려면: ./scripts/logs.sh" 