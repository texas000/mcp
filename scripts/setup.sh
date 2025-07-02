#!/bin/bash

echo "🔧 스크립트 파일들을 설정합니다..."

# scripts 디렉토리의 모든 .sh 파일에 실행 권한 부여
chmod +x scripts/*.sh

echo "✅ 모든 스크립트에 실행 권한이 부여되었습니다!"
echo ""
echo "📋 사용 가능한 스크립트:"
echo "  🚀 ./scripts/start.sh    - 서비스 시작"
echo "  🛑 ./scripts/stop.sh     - 서비스 중지"
echo "  🧹 ./scripts/clean.sh    - 완전 정리"
echo "  📋 ./scripts/logs.sh     - 로그 확인"
echo "  🔨 ./scripts/rebuild.sh  - 이미지 재빌드"
echo "  📊 ./scripts/status.sh   - 상태 확인"
echo "  🐚 ./scripts/shell.sh    - 컨테이너 접속"
echo ""
echo "🚀 서비스를 시작하려면: ./scripts/start.sh" 