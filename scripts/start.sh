#!/bin/bash

echo "🚀 FastAPI 개발 환경을 시작합니다..."

# 환경 변수 파일 확인
if [ ! -f .env ]; then
    echo "❌ .env 파일이 없습니다!"
    echo "📝 .env 파일을 생성하고 PostgreSQL 연결 정보를 입력해주세요."
    exit 1
fi

# Docker Compose로 서비스 시작
echo "📦 Docker 컨테이너를 시작합니다..."
docker-compose up -d

# 서비스 상태 확인
echo "🔍 서비스 상태를 확인합니다..."
docker-compose ps

echo ""
echo "✅ 서비스가 시작되었습니다!"
echo "🌐 API 문서: http://localhost:8000"
echo "🗄️  외부 PostgreSQL 데이터베이스에 연결됨"
echo ""
echo "📋 로그를 확인하려면: ./scripts/logs.sh"
echo "🛑 서비스를 중지하려면: ./scripts/stop.sh" 