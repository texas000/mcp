#!/bin/bash

echo "📊 Docker 서비스 상태를 확인합니다..."
echo ""

# Docker Compose 서비스 상태
echo "🔍 Docker Compose 서비스 상태:"
docker-compose ps

echo ""
echo "📈 시스템 리소스 사용량:"
echo ""

# 컨테이너별 리소스 사용량
echo "💾 메모리 사용량:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"

echo ""
echo "🌐 네트워크 정보:"
docker network ls | grep fastapi

echo ""
echo "📁 볼륨 정보:"
docker volume ls | grep fastapi 