## 1. 프로젝트 초기 환경 및 코딩 규칙 정의

**[프로젝트 명]**
UC-OMS (Unified Channel Order Management System)

**[기술 스택]**
* **백엔드:** Python 3.10+, FastAPI (Pydantic), SQLAlchemy 2.0+ (asyncpg), Alembic
* **데이터베이스:** PostgreSQL
* **보안 라이브러리:** Cryptography (API Key 암호화/복호화용)

**[코딩 규칙]**
1.  **아키텍처:** Layered Architecture (Router -> Service -> Repository/Model)를 엄격히 준수.
2.  **비동기:** DB 작업 및 외부 API 호출 로직은 모두 비동기(`async/await`)로 작성.
3.  **보안:** 민감 정보(API Key, Secret Key)는 반드시 **`cryptography.fernet`**을 사용하여 암호화/복호화 로직을 Service Layer에 포함하여 구현.
4.  **주석:** 모든 클래스와 함수에는 Docstring을 필수적으로 작성할 것.

**[초기 파일 구조 (Cursor IDE 생성 요청)]**
다음 디렉토리와 파일을 생성해 주세요.
uc-oms/

├── .env.example

├── requirements.txt

├── Dockerfile

├── docker-compose.yml

└── app/

├── main.py

├── core/

│   ├── config.py             # 기본 설정 로드

│   ├── security.py           # 암호화/복호화 모듈

│   └── database.py           # DB 세션 및 연결 설정

├── api/v1/

│   └── admin/

│       └── channels.py       # 관리자 채널 CRUD 라우터

├── models/

│   └── channel.py            # ChannelConfig ORM 모델

├── schemas/

│   └── channel.py            # ChannelConfig Pydantic 스키마

└── services/

└── channel_service.py    # 비즈니스 로직 및 암호화 처리
## 2. 핵심 모델 및 스키마 정의 (Channel Configuration)

**[목표]**
관리자 채널 등록을 위한 ORM 모델과 Pydantic 스키마를 정의합니다.

### A. ORM 모델 정의 (`app/models/channel.py`)
1.  **모델명:** `ChannelConfig`
2.  **필드:**
    * `id`: Primary Key, Integer
    * `name`: String (255), Unique
    * `provider_type`: String (50) - 채널 제공자 유형 (예: 'NAVER', 'COUPANG')
    * `api_key`: String (512) - **암호화된 키 저장용**
    * `secret_key`: String (512) - **암호화된 비밀 키 저장용**
    * `is_active`: Boolean, Default=True
    * `last_sync_at`: DateTime, Nullable

### B. Pydantic 스키마 정의 (`app/schemas/channel.py`)
1.  **`ChannelConfigBase`:** `name`, `provider_type`, `api_key`, `secret_key` 필드를 포함. (생성 및 업데이트 시 사용)
2.  **`ChannelConfigCreate`:** `ChannelConfigBase`를 상속받음.
3.  **`ChannelConfigRead`:** DB에서 읽기용 스키마. **`api_key`와 `secret_key` 필드는 제외**하고, `id`, `name`, `provider_type`, `is_active`, `last_sync_at`만 포함.

## 3. 보안 모듈 및 Service Layer 구현

**[목표]**
API Key의 안전한 저장을 위한 암호화 모듈과 이를 사용하는 Service Layer의 기본 골격을 구현합니다.

### A. 암호화 모듈 (`app/core/security.py`)
1.  **`SECRET_KEY`**를 `config.py`에서 로드하여 Fernet 객체를 초기화.
2.  두 가지 비동기 함수를 구현:
    * `encrypt_data(data: str) -> str`: 입력 문자열을 암호화하여 반환.
    * `decrypt_data(data: str) -> str`: 입력 문자열을 복호화하여 반환.

### B. 채널 서비스 로직 (`app/services/channel_service.py`)
1.  **클래스명:** `ChannelService`
2.  **의존성:** DB 세션 (`AsyncSession`)과 `app/core/security.py` 모듈을 사용.
3.  다음 비동기 메소드들을 포함하여 구현:
    * `create_channel(db: AsyncSession, data: ChannelConfigCreate) -> ChannelConfig`:
        * **로직:** 입력된 `api_key`와 `secret_key`를 **`encrypt_data`** 함수를 사용하여 암호화한 후 DB에 저장.
    * `get_channel(db: AsyncSession, channel_id: int) -> ChannelConfig | None`:
        * **로직:** DB에서 채널을 조회하여 반환. (복호화는 라우터에서 필요 시 처리)
    * `get_channels(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[ChannelConfig]`:
        * **로직:** 모든 채널 리스트 조회.

## 4. 관리자 채널 CRUD 라우터 구현

**[목표]**
Service Layer를 사용하여 관리자용 채널 설정 API 엔드포인트를 구현합니다.

### A. 라우터 파일 (`app/api/v1/admin/channels.py`)
1.  **FastAPI 라우터**를 정의하고 `/api/v1/admin/channels` 경로로 설정.
2.  모든 엔드포인트에는 **더미 관리자 인증 의존성** (`Depends(admin_auth)`)이 있다고 가정하고 구현.
3.  **POST /**: 새 채널을 생성하고 `ChannelConfigRead` 스키마로 응답.
4.  **GET /**: 채널 목록을 조회하고 `list[ChannelConfigRead]` 스키마로 응답.
5.  **GET /{channel_id}**: 특정 채널을 조회하고 `ChannelConfigRead` 스키마로 응답. (채널이 없으면 404 에러 반환)
6.  **PUT /{channel_id}**: 채널 정보를 업데이트하고 `ChannelConfigRead` 스키마로 응답.

### B. 암호화된 키 복호화 테스트 API (선택 사항)
* **GET /{channel_id}/keys**:
    * **목표:** 관리자가 등록된 채널의 API Key를 **테스트 목적으로 확인**할 수 있도록 구현.
    * **로직:** `ChannelService`를 통해 채널을 조회 $\rightarrow$ 암호화된 키를 **`decrypt_data`** 함수로 복호화 $\rightarrow$ 복호화된 키를 포함한 응답 (`{"api_key": "복호화된키", "secret_key": "복호화된시크릿"}`)을 반환. (실제 운영에서는 매우 제한적으로 사용해야 함.)