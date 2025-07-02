# FastAPI Sample Project

간단한 FastAPI 샘플 프로젝트입니다.

## 설치

필요한 패키지들을 설치하세요:

```bash
pip install -r requirements.txt
```

## 실행

### 로컬 실행

서버를 실행하려면:

```bash
# 방법 1: uvicorn 직접 사용
uvicorn main:app --reload

# 방법 2: Python 스크립트 실행
python main.py
```

### Docker를 사용한 실행 (권장)

Docker를 사용하여 FastAPI 애플리케이션을 실행 (외부 PostgreSQL 데이터베이스 연결):

#### 사전 준비
1. 프로젝트 루트에 `.env` 파일을 생성하고 PostgreSQL 연결 정보를 입력하세요:
```bash
POSTGRES_URL=your_postgresql_url
POSTGRES_URL_NON_POOLING=your_postgresql_url_non_pooling
POSTGRES_USER=your_username
POSTGRES_HOST=your_host
POSTGRES_PASSWORD=your_password
POSTGRES_DATABASE=your_database
POSTGRES_URL_NO_SSL=your_postgresql_url_no_ssl
POSTGRES_PRISMA_URL=your_prisma_url
```

#### 스크립트 사용 (권장)
```bash
# 스크립트 설정 (최초 1회)
chmod +x scripts/*.sh

# 서비스 시작
./scripts/start.sh

# 로그 확인
./scripts/logs.sh

# 서비스 중지
./scripts/stop.sh

# 완전 정리
./scripts/clean.sh
```

#### 직접 명령어 사용
```bash
# FastAPI 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f app

# 서비스 중지
docker-compose down
```

서버가 실행되면 다음 URL에서 접근할 수 있습니다:
- API 서버: http://localhost:8000
- API 문서: http://localhost:8000/docs
- ReDoc 문서: http://localhost:8000/redoc
- MCP 서버: http://localhost:8000/mcp

## API 엔드포인트

### 기본 엔드포인트
- `GET /`: API 문서로 리다이렉트
- `GET /health`: API 상태 확인

### 데이터베이스 엔드포인트
- `GET /db/test-connection`: 데이터베이스 연결 테스트
- `GET /db/config`: 데이터베이스 설정 정보 확인 (비밀번호는 가려짐)
- `GET /db/tables`: 데이터베이스의 모든 테이블 목록 조회
- `GET /db/table/{table_name}`: 특정 테이블의 구조 정보 조회
- `GET /db/table/{table_name}/data`: 특정 테이블의 데이터 조회 (limit, offset 파라미터 지원)

### 노트 관리 엔드포인트 (MCP 통합)
- `POST /notes`: 새로운 노트 생성 (사용자가 "노트" 언급 시 사용)
- `GET /notes`: 모든 노트 조회 (페이징 지원)
- `GET /notes/{note_id}`: 특정 노트 조회
- `DELETE /notes/{note_id}`: 특정 노트 삭제

## MCP (Model Context Protocol) 사용법

이 프로젝트는 FastAPI MCP를 통합하여 MCP 클라이언트와 연결할 수 있습니다.

### MCP 클라이언트 연결

#### SSE를 사용한 연결
가장 인기 있는 MCP 클라이언트(Claude Desktop, Cursor & Windsurf)는 다음 설정을 사용합니다:

```json
{
  "mcpServers": {
    "fastapi-mcp": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

#### mcp-remote를 사용한 연결
인증이나 SSE를 지원하지 않는 MCP 클라이언트의 경우 `mcp-remote`를 브리지로 사용할 수 있습니다:

```json
{
  "mcpServers": {
    "fastapi-mcp": {
      "url": "https://mcp-rosy.vercel.app/mcp"
    }
  }
}
```

### MCP 서버 접근
- MCP 서버는 `http://localhost:8000/mcp`에서 실행됩니다
- FastAPI 애플리케이션과 함께 자동으로 시작됩니다

## 개발

이 프로젝트는 FastAPI 프레임워크를 사용하여 구축되었습니다. 자동으로 생성되는 API 문서를 통해 엔드포인트를 테스트할 수 있습니다. 