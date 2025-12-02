from fastapi import FastAPI, APIRouter
from app.api.v1.admin.channels import router as channel_router
from app.core.database import Base, engine
from app.core.config import settings

# 1. FastAPI 애플리케이션 인스턴스 생성 및 설정
app = FastAPI(
    title="UOMS API", 
    description="통합 주문 관리 시스템 백엔드 API",
    version="0.0.3",
    docs_url="/docs",       # Swagger UI 경로
    redoc_url="/redoc"      # ReDoc 문서 경로
)

# 2. 데이터베이스 테이블 초기화 (선택적)
# 애플리케이션 시작 시점에 ORM 모델에 정의된 테이블이 DB에 존재하는지 확인하고 생성합니다.
# NOTE: Alembic과 같은 DB 마이그레이션 툴 사용 시 이 코드는 주석 처리하거나 제거해야 합니다.
#def create_db_tables():
#    """
#    SQLAlchemy Base와 Engine을 사용하여 모든 모델의 테이블을 생성합니다.
#    """
#    try:
#        # models에서 정의된 모든 테이블을 DB에 생성합니다. (models 파일들을 import 해야 Base가 인식함)
#        from models import channel # channel 모델을 import 하여 Base에 등록
#        Base.metadata.create_all(bind=engine)
#        print("Database tables created successfully (if not already existing).")
#    except Exception as e:
#        print(f"Error creating database tables: {e}")

# 3. 라우터 포함 (경로 설정)
# 모든 API는 /api/v1/ 접두어를 사용하여 버전 관리를 합니다.
API_V1_PREFIX = "/api/v1"

# 3.1. 관리자 API 라우터 포함
admin_router = APIRouter(prefix="/admin")
admin_router.include_router(channel_router) # /admin/channels 로 경로 설정

# 3.2. 메인 애플리케이션에 라우터 연결
app.include_router(admin_router, prefix=API_V1_PREFIX)

# 5. 루트 경로 (선택적)
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "UOMS API is running!", "version": app.version}