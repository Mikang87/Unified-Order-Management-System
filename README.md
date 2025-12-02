# 🌐 통합 주문 관리 시스템 (Unified Order Management System, UOMS)

## 🚀 프로젝트 개요 (Project Overview)
**여러 이커머스 채널(스마트 스토어, 쿠팡 등)의 주문 데이터를 통합하여 단일 대시보드에서 관리할 수 있는 중앙 집중식 관리 시스템 구축. 관리자 측면의 기능(API 연동, 데이터 표준화, CRUD) 구현에 중점을 둔 백엔드 개발 프로젝트입니다.**

## 🌟 프로젝트 하이라이트
1. **다중 API 통합:** 서로 다른 외부 쇼핑몰 API를 표준화된 단일 데이터 모델로 통합 처리.
2. **확장 가능한 관리자 시스템:** 관리자가 직접 새로운 채널을 등록/수정/비활성화할 수 있는 동적 설정 기능 구현
3. **보안:** 민감한 API 및 Secret은 안전하게 암호화하여 저장 및 관리

## 개발 기간
2025.11.18~

## 현재 버전
**v0.0.3** | 비동기 데이터베이스 마이그레이션 완료, 초기 실행 설정 정리

## 🛠️ 기술 스택 (Tech Stack)
1. **Python3.14** | 주력 개발 언어 및 환경, 백엔드 로직 구현.  
2. **FastAPI** | 비동기 API 웹 프레임워크, 높은 성능의 API 서버 구현, 자동 문서화(Swagger/OpenAPI) 제공.  
3. **Pydantic** | 데이터 유효성 검사 및 모델링 라이브러리, API 요청/응답 데이터에 대한 강력한 유효성 검사 및 스키마 정의.
4. **Uvicorn** | FastAPI를 실행하는 비동기 서버, 실제 프로덕션 환경에서 애플리케이션 서비스 제공.
5. **MySQL** | 데이터베이스 서버. 채널 설정 및 주문 데이터와 같은 프로젝트 데이터를 영구 저장.
6. **SQLalchemy** | Python ORM, Python 객체를 통해 데이터베이스와 상호작용.
7. **Docker** | 컨테이너화 도구, 개발 환경과 배포 환경을 일치시키고 애플리케이션을 격리하여 실행.

## 📂 프로젝트 구조 및 핵심 기능 구현 현황
1. 관리자 채널 설정 (Admin Channel Configuration) (완료)  
<img width="1902" height="962" alt="image" src="https://github.com/user-attachments/assets/afc39f87-3926-475d-a83d-e2d60ed949d7" />

3. 주문 데이터 통합 및 수집 (Order Integration & Collector)

4. 주문 관리 및 모니터링 (Order Management & Monitoring)

## 파일 구조
uc-oms/

├── .env.example  
├── requirements.txt  
├── Dockerfile  
├── docker-compose.yml  
├── grand_remote_access.sh  
├── alembic.ini  
│  
├── alembic/  
│   ├── versions/  
│   │   ├── 5c7b62e589f9_create_channel_configs_table.py  
│   │   ├── aefc57bcea3d_initial_database_setup.py  
│   │   └── b0a31c003a59_initial_schema_setup.py  
│   └── env.py  
│  
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
    └── channel_service.py    

## 프로젝트 구동 가이드  
**1. 전제조건**  
>프로젝트를 실행하려면 시스템에 다음 소프트웨어가 설치되어 있어야 합니다.  
>+ **Git:** 소스 코드 클론을 위해 필요합니다.  
>+ **Docker 및 Docker Compose:** 애플리케이션 및 MySQL 데이터베이스 컨테이너를 빌드하고 실행하기 위해 필요합니다.

**2. 프로젝트 초기 설정**  
>**2.1. 소스 코드 다운로드**
```bash
git clone https://github.com/Mikang87/Unified-Order-Management-System  
cd uc-oms
```
>**2.2. 환경 설정 파일(.env) 생성 및 수정(필수)**  
> >.env 파일은 데이터베이스 연결 정보, 비밀 키 등 개인 설정 정보를 담고 있으므로, .env.example 파일을 복사하여 사용합니다.
> >1. .env.example 파일을 복사하여 .env 파일을 생성합니다.
```bash 
cp .env.example .env
```
> >3. .env 파일을 열고 다음 필수 변수를 설정합니다.  
> >**MYSQL_USER:**
> >**MYSQL_PASSWORD:**
> >**MYSQL_HOST:**
> >**MYSQL_DATABASE:**
> >**SECRET_KEY:**

**3. Docker Compose 실행**
>모든 설정이 완료되면, Docker Compose를 사용하여 웹 서버와 데이터베이스를 함께 구동합니다.
>**3.1. 이미지 빌드**
>Dockerfile과 requirement.txt에 정의된 의존성을 기반으로 웹 서버 이미지를 빌드합니다.
```bash
docker-compose build --no-cache web
```
>**3.2 컨테이너 실행**
>MySQL 데이터베이스와 Uvicorn 웹 서버 컨테이너를 실행하고 연결합니다.
```bash
docker-compose up
```
**4. 구동 확인 및 API 접속**  
>컨테이너가 성공적으로 시작되면 웹서버(uc-oms-web-1) 로그에 Application startup complete. 메시지가 출력됩니다.  
>서버 상태: http://localhost:8000 | 서버의 기본 상태 메시지를 확인합니다.  
>API 문서: http://localhost:8000/docs | FastAPI의 자동 생성된 Swagger UI를 통해 API 엔드포인트 목록을 확인합니다.  

## 🛑 TroubleShooting

**25.12.02**
**비동기 데이터베이스 마이그레이션을 위한 초기 설정**
>초기 설정에 마이그레이션 스크립트가 부재해 최초 테이블 생성에 오류가 발생 | init alembic으로 초기화 및 alembic revision 명령어로 프로젝트의 alembic/versions 폴더에 스크립트 파일을 생성하여 프로젝트 파일에 추가
---
**25.11.22**  
**1. MySQL 인증 오류(Initial Setup)**  
>**MySQL 연결** | DB 비밀번호에 특정 특수문자(@)가 포함되어 MySQL 초기 설정에서 문제 발생(MySQL 8.0의 보안 강화로 추정) -> 다른 조합으로 비밀번호 변겅.  
>**원격 접근** | DB 컨테이너 초기화 시점에 애플리케이션 컨테이너가 먼저 시작되어 연결 오류 발생 -> web 서비스 커맨드에 sleep 30을 추가하여 DB 시작 대기 시간 확보.  
>            | MySQL 8.0에서 기본 인증 방식이 변겅됨. -> grant_remote_access.sh를 수정하여 mysql_native_password 인증 방식을 명시적으로 설정.  

**25.11.19**  
**1. MySQL 드라이버 관련 오류(NoSuchModuleError)**  
>sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:mysql.mysqldb  
>빌드에 필요한 C 라이브러리 부족으로 판단되어 mysqlclient 대신 pymysql 드라이버를 사용하도록 변경함.  
  
**2. Python 모듈 임포트 오류(ImportError)**  
>ImportError: cannot import name 'ChannelCreate' from 'schemas.channel'  
>Schema 파일의 클래스 이름과 임포트 하는 클래스 이름의 불일치 문제. 임포트하는 파일(app/services/channel_service.py, app/api/v1/admin/channels.py)에서의 클래스 이름을 스키마 파일에서 정의된 실제 이름으로 통일함.

---
**25.11.22**  
**1. MySQL 인증 오류(Initial Setup)**  
>**MySQL 연결** | DB 비밀번호에 특정 특수문자(@)가 포함되어 MySQL 초기 설정에서 문제 발생(MySQL 8.0의 보안 강화로 추정) -> 다른 조합으로 비밀번호 변겅.  
>**원격 접근** | DB 컨테이너 초기화 시점에 애플리케이션 컨테이너가 먼저 시작되어 연결 오류 발생 -> web 서비스 커맨드에 sleep 30을 추가하여 DB 시작 대기 시간 확보.  
>            | MySQL 8.0에서 기본 인증 방식이 변겅됨. -> grant_remote_access.sh를 수정하여 mysql_native_password 인증 방식을 명시적으로 설정.  

**2. Pydantic 스키마 및 필드명 불일치**  
> API 요청 본문과 내부 Pydnatic 모델, DB ORM 모델 간의 필드명 불일치 해소  

## 🤝 기여자 및 라이선스

| **백진명** | 프로젝트 리드 개발 및 설계 | [Mikang87](https://github.com/Mikang87) |

License: <**MIT License**>

---

## 💭 향후 계획 및 개선 사항

* **Frontend 개발:** React 또는 Vue를 사용하여 주문 목록 및 채널 관리 페이지 대시보드 구현.
