#!/bin/bash

echo "📋 Docker 로그를 확인합니다..."
echo ""

# 사용자에게 로그 옵션 제공
echo "어떤 로그를 확인하시겠습니까?"
echo "1) FastAPI 앱 로그"
echo "2) 실시간 로그 (follow)"
echo ""

read -p "선택하세요 (1-2): " choice

case $choice in
    1)
        echo "📋 FastAPI 앱 로그를 표시합니다..."
        docker-compose logs app
        ;;
    2)
        echo "📋 실시간 로그를 표시합니다 (Ctrl+C로 종료)..."
        docker-compose logs -f app
        ;;
    *)
        echo "❌ 잘못된 선택입니다. FastAPI 앱 로그를 표시합니다..."
        docker-compose logs app
        ;;
esac 