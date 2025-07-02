from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, text, MetaData, inspect
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv
from typing import List, Dict, Any

# .env 파일 로드
load_dotenv()

app = FastAPI(title="RYAN MCP SERVER", description="RYAN PERSONAL MCP SERVER")

# Create an MCP server based on this app
mcp = FastApiMCP(app)

# Mount the MCP server directly to your app
mcp.mount()

def get_database_connection():
    """데이터베이스 연결을 생성합니다."""
    try:
        # 개별 환경 변수에서 데이터베이스 정보 가져오기
        postgres_user = os.getenv("POSTGRES_USER")
        postgres_password = os.getenv("POSTGRES_PASSWORD")
        postgres_host = os.getenv("POSTGRES_HOST")
        postgres_database = os.getenv("POSTGRES_DATABASE")
        
        # 필수 환경 변수 확인
        if not all([postgres_user, postgres_password, postgres_host, postgres_database]):
            # POSTGRES_URL이 있으면 사용
            postgres_url = os.getenv("POSTGRES_URL")
            if postgres_url:
                engine = create_engine(postgres_url)
                return engine
            else:
                raise HTTPException(
                    status_code=500, 
                    detail="Database configuration incomplete. Please set POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DATABASE or POSTGRES_URL"
                )
        
        # 개별 환경 변수로 연결 문자열 구성
        postgres_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_database}"
        
        engine = create_engine(postgres_url)
        return engine
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/db/tables", response_model=List[str])
async def get_tables():
    """데이터베이스의 모든 테이블 목록을 반환합니다."""
    try:
        engine = get_database_connection()
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return tables
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tables: {str(e)}")

@app.get("/db/table/{table_name}")
async def get_table_info(table_name: str):
    """특정 테이블의 정보를 반환합니다."""
    try:
        engine = get_database_connection()
        inspector = inspect(engine)
        
        # 실제 테이블명 목록 가져오기 (대소문자 구분)
        available_tables = inspector.get_table_names()
        
        # 테이블 존재 여부 확인 (대소문자 무시)
        table_found = False
        actual_table_name = table_name
        
        # 정확한 테이블명 찾기
        for table in available_tables:
            if table.lower() == table_name.lower():
                actual_table_name = table
                table_found = True
                break
        
        if not table_found:
            raise HTTPException(
                status_code=404, 
                detail=f"Table '{table_name}' not found. Available tables: {available_tables}"
            )
        
        # 테이블 컬럼 정보 (안전하게 변환)
        columns_info = []
        try:
            columns = inspector.get_columns(actual_table_name)
            for col in columns:
                # 컬럼 정보를 딕셔너리로 안전하게 변환
                col_dict = {
                    "name": col.get("name", ""),
                    "type": str(col.get("type", "")),
                    "nullable": col.get("nullable", True),
                    "default": str(col.get("default", "")),
                    "primary_key": col.get("primary_key", False)
                }
                columns_info.append(col_dict)
        except Exception as col_error:
            columns_info = [{"error": f"Failed to get column info: {str(col_error)}"}]
        
        # 테이블 제약 조건 (안전하게 변환)
        constraints_info = []
        try:
            constraints = inspector.get_unique_constraints(actual_table_name)
            for constraint in constraints:
                constraint_dict = {
                    "name": constraint.get("name", ""),
                    "column_names": constraint.get("column_names", [])
                }
                constraints_info.append(constraint_dict)
        except Exception as constraint_error:
            constraints_info = [{"error": f"Failed to get constraint info: {str(constraint_error)}"}]
        
        # 외래 키 정보 (안전하게 변환)
        foreign_keys_info = []
        try:
            foreign_keys = inspector.get_foreign_keys(actual_table_name)
            for fk in foreign_keys:
                fk_dict = {
                    "name": fk.get("name", ""),
                    "constrained_columns": fk.get("constrained_columns", []),
                    "referred_table": fk.get("referred_table", ""),
                    "referred_columns": fk.get("referred_columns", [])
                }
                foreign_keys_info.append(fk_dict)
        except Exception as fk_error:
            foreign_keys_info = [{"error": f"Failed to get foreign key info: {str(fk_error)}"}]
        
        return {
            "table_name": actual_table_name,
            "requested_table": table_name,
            "columns": columns_info,
            "constraints": constraints_info,
            "foreign_keys": foreign_keys_info
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get table info: {str(e)}")

@app.get("/db/table/{table_name}/data")
async def get_table_data(table_name: str, limit: int = 10, offset: int = 0):
    """특정 테이블의 데이터를 반환합니다."""
    try:
        engine = get_database_connection()
        inspector = inspect(engine)
        
        # 실제 테이블명 목록 가져오기 (대소문자 구분)
        available_tables = inspector.get_table_names()
        
        # 테이블 존재 여부 확인 (대소문자 무시)
        table_found = False
        actual_table_name = table_name
        
        # 정확한 테이블명 찾기
        for table in available_tables:
            if table.lower() == table_name.lower():
                actual_table_name = table
                table_found = True
                break
        
        if not table_found:
            raise HTTPException(
                status_code=404, 
                detail=f"Table '{table_name}' not found. Available tables: {available_tables}"
            )
        
        with engine.connect() as connection:
            # 안전한 쿼리 구성 (테이블명을 따옴표로 감싸기)
            query = text(f'SELECT * FROM "{actual_table_name}" LIMIT {limit} OFFSET {offset}')
            result = connection.execute(query)
            
            # 컬럼명 가져오기 (리스트로 변환)
            columns = list(result.keys())
            
            # 데이터를 딕셔너리 리스트로 변환
            data = []
            for row in result.fetchall():
                row_dict = {}
                for i, value in enumerate(row):
                    # None 값과 특수 타입 처리
                    if value is None:
                        row_dict[columns[i]] = None
                    elif hasattr(value, 'isoformat'):  # datetime 객체
                        row_dict[columns[i]] = value.isoformat()
                    else:
                        row_dict[columns[i]] = str(value)
                data.append(row_dict)
            
            return {
                "table_name": actual_table_name,
                "requested_table": table_name,
                "data": data,
                "limit": limit,
                "offset": offset,
                "total_rows": len(data)
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get table data: {str(e)}")

@app.get("/db/test-connection")
async def test_database_connection():
    """데이터베이스 연결을 테스트합니다."""
    try:
        engine = get_database_connection()
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            return {
                "status": "connected",
                "message": "Database connection successful",
                "version": version
            }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.get("/db/config")
async def get_database_config():
    """데이터베이스 설정 정보를 반환합니다 (비밀번호는 가려짐)."""
    try:
        postgres_user = os.getenv("POSTGRES_USER")
        postgres_host = os.getenv("POSTGRES_HOST")
        postgres_database = os.getenv("POSTGRES_DATABASE")
        postgres_password = os.getenv("POSTGRES_PASSWORD")
        
        # 비밀번호 마스킹
        masked_password = "*" * len(postgres_password) if postgres_password else None
        
        return {
            "user": postgres_user,
            "host": postgres_host,
            "database": postgres_database,
            "password": masked_password,
            "has_url": bool(os.getenv("POSTGRES_URL")),
            "has_individual_config": all([postgres_user, postgres_host, postgres_database, postgres_password])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get database config: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 