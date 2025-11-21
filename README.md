# 🌐 통합 주문 관리 시스템 (Unified Order Management System, UOMS)

## 🚀 프로젝트 개요 (Project Overview)
**여러 이커머스 채널(스마트 스토어, 쿠팡 등)의 주문 데이터를 통합하여 단일 대시보드에서 관리할 수 있는 중앙 집중식 관리 시스템 구축. 관리자 측면의 기능(API 연동, 데이터 표준화, CRUD) 구현에 중점을 둔 백엔드 개발 프로젝트입니다.**

## 🌟 프로젝트 하이라이트
1. **다중 API 통합:** 서로 다른 외부 쇼핑몰 API를 표준화된 단일 데이터 모델로 통합 처리.
2. **확장 가능한 관리자 시스템:** 관리자가 직접 새로운 채널을 등록/수정/비활성화할 수 있는 동적 설정 기능 구현
3. **보안:** 민감한 API 및 Secret은 안전하게 암호화하여 저장 및 관리

## 개발 기간
2025.11.18~

## 🛠️ 기술 스택 (Tech Stack)
1. **API 프레임워크:** Python3.14 FastAPI | 높은 성능의 비동기 API 서버 구현 및 Pydantic을 활용한 강력한 데이터 유효성 검사.
2. **데이터베이스:** MySQL |
3. **컨테이너:** Docker | 개발 환경 구축 및 배포 환경 구성을 위한 컨테이너화

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

## 🛑 TroubleShooting
**1. MySQL 드라이버 관련 오류(NoSuchModuleError)**  
  sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:mysql.mysqldb  
  빌드에 필요한 C 라이브러리 부족으로 판단되어 mysqlclient 대신 pymysql 드라이버를 사용하도록 변경함.  
  
**2. Python 모듈 임포트 오류(ImportError)**  
  ImportError: cannot import name 'ChannelCreate' from 'schemas.channel'  
  Schema 파일의 클래스 이름과 임포트 하는 클래스 이름의 불일치 문제. 임포트하는 파일(app/services/channel_service.py, app/api/v1/admin/channels.py)에서의 클래스 이름을 스키마 파일에서 정의된 실제 이름으로 통일함.  

## 🤝 기여자 및 라이선스

| **백진명** | 프로젝트 리드 개발 및 설계 | [Mikang87](https://github.com/Mikang87) |

License: <**MIT License**>

---

## 💭 향후 계획 및 개선 사항

* **Frontend 개발:** React 또는 Vue를 사용하여 주문 목록 및 채널 관리 페이지 대시보드 구현.
