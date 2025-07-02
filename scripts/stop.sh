#!/bin/bash

echo "🛑 FastAPI 개발 환경을 중지합니다..."

# Docker Compose로 서비스 중지
echo "📦 Docker 컨테이너를 중지합니다..."
docker-compose down

echo ""
echo "✅ 서비스가 중지되었습니다!"
echo ""
echo "🚀 서비스를 다시 시작하려면: ./scripts/start.sh"
echo "🧹 완전히 정리하려면: ./scripts/clean.sh" 