# 🌐 통합 주문 관리 시스템 (Unified Order Management System, UOMS)

## 🚀 프로젝트 개요 (Project Overview)
**본 프로젝트는 여러 이커머스 채널(스마트스토어, 쿠팡 등)의 주문 및 상품 데이터를 통합하여 단일 시스템에서 관리할 수 있는 중앙 집중식 백엔드 시스템 구축 프로젝트입니다. 관리자가 채널을 직접 등록하고, 표준화된 API 인터페이스(Collector Pattern)를 통해 외부 쇼핑몰의 데이터를 주기적으로 수집할 수 있는 기능 구현에 중점을 두었습니다.**

## 🌟 프로젝트 하이라이트
1. **다중 채널 통합 및 표준화:** 서로 다른 외부 쇼핑몰 API를 표준화된 단일 데이터 모델로 통합하여 처리합니다.
2. **확장 가능한 관리자 시스템:** 관리자가 직접 새로운 채널을 등록/수정/비활성화할 수 있으며, 이 설정에 따라 동적으로 주문 및 상품 수직 로직이 실행됩니다.
3. **비동기 기능:** FastAPI와 SQLAlchemy의 비동기 기능을 활용하여 외부 API 호출 및 DB 트랜잭션을 효율적으로 처리합니다.  
4. **보안:** 민감한 API 및 Secret은 Fernet 암호화를 사용하여 DB에 안전하게 저장 및 관리됩니다.  
5. **데이터 무결성:** 주문 데이터 수집 시, external_order_id 및 external_item_id를 기준으로 UPSERT(Update or Insert) 로직을 구현하여 데이터 중복을 방지하고 상태 변경을 효율적으로 처리합니다.

## 개발 기간
2025.11.18~2025.12.07

## 현재 버전
**v1.0.0** | UMOS 핵심 백엔드 기능(Channel, Product Fetch, Order Fetch/UPSERT) 구현 완료.

## 🛠️ 기술 스택 (Tech Stack)
1. **Python3.14** | 주력 개발 언어 및 환경, 백엔드 로직 구현.  
2. **FastAPI** | 비동기 API 웹 프레임워크, 높은 성능의 API 서버 구현, 자동 문서화(Swagger/OpenAPI) 제공.  
3. **httpx** | 외부 쇼핑몰 API와의 비동기 통신 처리
4. **Pydantic** | 데이터 유효성 검사 및 모델링 라이브러리, API 요청/응답 데이터에 대한 강력한 유효성 검사 및 스키마 정의.
5. **Uvicorn** | FastAPI를 실행하는 비동기 서버, 실제 프로덕션 환경에서 애플리케이션 서비스 제공.
6. **MySQL** | 데이터베이스 서버. 채널 설정 및 주문 데이터와 같은 프로젝트 데이터를 영구 저장.
7. **SQLalchemy** | Python ORM, Python 객체를 통해 데이터베이스와 상호작용.
8. **Alembic** | 비동기 데이터베이스 마이그레이션.
9. **Docker** | 컨테이너화 도구, 개발 환경과 배포 환경을 일치시키고 애플리케이션을 격리하여 실행.
10. **Fernet** | API key 암호화 및 비밀번호 해싱

## 📂 시스템 아키텍처 (System Architecture)  
UOMS는 3계층 아키텍처(Presentation - Service - Data/External)와 Collector Pattern을 결합하여 구축되었습니다.
1. API Layer (Presentation):   
+ FastAPI 라우터(/api/v1/admin/channels, /products, /orders)가 외부 요청을 처리합니다.  

2. Service Layer (Buisness Logic):  
+ ChannelService, ProductCollectorService, OrderService가 존재합니다.  
+ OrderService는 채널 설정을 조회하고, 적절한 IOrderCollector를 선택하여 주문을 수집한 후, UPSERT 로직을 통해 DB에 데이터를 저장합니다.  

3. Data Layer:  
+ ORM 모델(ChannelConfig, Order, OrderItem)을 통해 DB 데이터를 관리합니다.  
+ Collecter Pattern: IProductCollector, IOrderCollctor와 같은 추상 인터페이스를 정의하고, CoupangCollector, SmartstoreCollector 등의 클래스가 이를 구현하여 채널별 API 통신 로직을 분리합니다.  


## 파일 구조   
uc-oms/    
├── .env   
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
    │       ├── channels.py       # 관리자 채널 CRUD 라우터   
    │       ├── products.py`      # 상품 목록 조회 라우터   
    │       └── orders.py         # 주문 조회 라우터  
    ├── models/
    │   ├── channel.py            # ChannelConfig ORM 모델    
    │   └── order.py              # 주문 ORM 모델     
    ├── schemas/   
    │   ├── channel.py            # ChannelConfig Pydantic 스키마   
    │   └── order.py              # Order Pydantic 스키마   
    ├── collectors                # API를 통한 상품 목록 조회   
    │   ├── base_collector.py     # 모든 외부 채널의 상품 조회 API를 위한 추상 인터페이스   
    │   ├── coupang_collector.py  # coupang 컬렉터   
    │   ├── smartstore_collector.py  # smartstore 컬렉터   
    │   └── mock_collector.py     # 테스트용(Mock) 컬렉터   
    └── services/    
        ├── channel_service.py     
        ├── product_service.py   
        └── order_service.py   

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
cp .example .env
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

+ **Frontend 개발:** React 또는 Vue를 사용하여 주문 목록 및 채널 관리 페이지 대시보드 구현.
+ **쇼핑몰 API 추가:** 현재 구현된 Coupang, Smartstore 이외의 다른 쇼핑몰 API 인터페이스의 표준화
