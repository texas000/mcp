#!/bin/bash

echo "🧹 FastAPI 개발 환경을 완전히 정리합니다..."

# 서비스 중지 및 볼륨 삭제
echo "📦 Docker 컨테이너와 볼륨을 삭제합니다..."
docker-compose down -v

# 사용하지 않는 이미지 정리
echo "🗑️  사용하지 않는 Docker 이미지를 정리합니다..."
docker image prune -f

# 사용하지 않는 네트워크 정리
echo "🌐 사용하지 않는 Docker 네트워크를 정리합니다..."
docker network prune -f

echo ""
echo "✅ 환경이 완전히 정리되었습니다!"
echo ""
echo "🚀 새로 시작하려면: ./scripts/start.sh" 