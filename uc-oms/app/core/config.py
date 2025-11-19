from typing import Any
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict # pydantic v2 이상에서는 pydantic_settings 사용

# 1. BaseSettings 상속을 통해 환경 변수를 로드할 설정 클래스 정의
class Settings(BaseSettings):
    # Pydantic SettingsConfigDict를 사용하여 환경 설정 지정
    model_config = SettingsConfigDict(
        env_file='.env', 
        extra='ignore' # .env 파일에 정의되지 않은 변수는 무시
    )

    # ==================
    # Database Settings
    # ==================
    # Field(env='...')를 사용하여 환경 변수 이름과 클래스 변수 이름이 다를 때 매핑 가능
    MYSQL_USER: str = Field(..., env='MYSQL_USER')
    MYSQL_PASSWORD: str = Field(..., env='MYSQL_PASSWORD')
    MYSQL_HOST: str = Field(..., env='MYSQL_HOST')
    MYSQL_DATABASE: str = Field(..., env='MYSQL_DATABASE')
    
    # ==================
    # Security Settings
    # ==================
    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    ALGORITHM: str = Field("HS256", env='ALGORITHM')
    
    # ==================
    # Application Settings
    # ==================
    # DEBUG 모드 여부 등 추가 설정 (예시)
    DEBUG: bool = False


    # 2. computed property를 사용하여 SQLAlchemy URL 생성
    @property
    def DATABASE_URL(self) -> str:
        """
        개별 DB 설정 변수들을 조합하여 SQLAlchemy에서 사용할 연결 URL을 반환합니다.
        """
        # driver://user:password@host/database
        # mysqlclient를 사용한다고 가정하고 'mysql://' 대신 'mysql+mysqlclient://'를 사용해도 됩니다.
        return f"mysql+mysqlclient://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}/{self.MYSQL_DATABASE}"
        
        # MySQL 8.0 이상에서 Caching SHA2 인증 문제 발생 시: 
        # return f"mysql+mysqlclient://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}/{self.MYSQL_DATABASE}?charset=utf8mb4"


# 3. 애플리케이션 전체에서 사용할 설정 객체 인스턴스 생성
settings = Settings()

# settings.DATABASE_URL 을 통해 어디서든 DB URL에 접근 가능