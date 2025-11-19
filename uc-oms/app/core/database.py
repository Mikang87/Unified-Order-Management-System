from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings

# 1. Engine 생성
# settings.DATABASE_URL: config.py에서 정의한 DB 연결 URL (예: 'mysql+mysqlclient://user:pass@host/db')
# pool_pre_ping=True: DB 연결이 끊어졌을 때 자동으로 재접속을 시도하여 연결 유효성을 검사합니다.
engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True, 
    # echo=True # 개발 단계에서는 SQL 쿼리를 터미널에 출력하여 디버깅에 도움을 줄 수 있습니다.
)

# 2. SessionLocal 설정
# autocommit=False: 트랜잭션 수동 관리 (커밋할 때까지 변경사항 반영 안 됨)
# autoflush=False: 커밋 없이도 변경사항을 DB에 전달하지 않음
# bind=engine: 생성한 DB 엔진에 바인딩
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# 3. Base (선언적 기본 클래스) 정의
# 이 클래스를 상속받아 모든 ORM 모델(Table)을 정의하게 됩니다.
Base = declarative_base()


# 4. FastAPI Dependency: 요청별 DB 세션을 제공하는 함수
# 이 함수는 FastAPI의 Dependency Injection 시스템을 통해 사용됩니다.
def get_db():
    """
    각 API 요청마다 독립적인 DB 세션을 생성하고, 요청 처리가 끝난 후 세션을 닫아 자원을 해제합니다.
    """
    db = SessionLocal() # 새로운 세션 생성
    try:
        # FastAPI 엔드포인트에 세션을 제공
        yield db
    finally:
        # 요청 처리가 완료되면(성공/실패 무관) 세션을 닫습니다.
        db.close()