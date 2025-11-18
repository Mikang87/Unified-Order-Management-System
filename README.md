## 🌐 통합 주문 관리 시스템 (Unified Order Management System, UOMS)

## 🚀 프로젝트 개요 (Project Overview)
**여러 이커머스 채널(스마트 스토어, 쿠팡 등)의 주문 데이터를 통합하여 단일 대시보드에서 관리할 수 있는 중앙 집중식 관리 시스템 구축. 관리자 측면의 기능(API 연동, 데이터 표준화, CRUD) 구현에 중점을 둔 백엔드 개발 프로젝트입니다.**

## 🌟 프로젝트 하이라이트
**다중 API 통합:** 서로 다른 외부 쇼핑몰 API를 표준화된 단일 데이터 모델로 통합 처리.
**확장 가능한 관리자 시스템:** 관리자가 직접 새로운 채널을 등록/수정/비활성화할 수 있는 동적 설정 기능 구현
**보안:** 민감한 API 및 Secreat은 안전하게 암화화하여 저장 및 관리

## 개발 기간
2025.11.18~

## 🛠️ 기술 스택 (Tech Stack)
**API 프레임워크:** Python3.14 FastAPI | 높은 성능의 비동기 API 서버 구현 및 Pydantic을 활용한 강력한 데이터 유효성 검사.
**데이터베이스:** MySQL |
**컨테이너:** Docker | 개발 환경 구축 및 배포 환경 구성을 위한 컨테이너화

## 📂 프로젝트 구조 및 핵심 기능 구현 현황
1. 관리자 채널 설정 (Admin Channel Configuration)

2. 주문 데이터 통합 및 수집 (Order Integration & Collector)

3. 주문 관리 및 모니터링 (Order Management & Monitoring)

🏃 시작하는 방법 (Getting Started)

## Prerequisites
* Docker 및 Docker Compose
* Python 3.14

1.  **Repository Clone:**
    ```bash
    git clone <저장소 URL>
    cd uc-oms
    ```
2.  **환경 설정:**
    * `.env.example` 파일을 복사하여 `.env`를 생성하고 DB 접속 정보 및 JWT Secret Key 등을 설정합니다.
3.  **Docker Compose 실행:**
    ```bash
    docker-compose up --build -d
    ```
4.  **DB 마이그레이션 적용:**
    ```bash
    # alembic을 사용했을 경우 명령어 명시 (예시)
    docker exec -it uc_oms_app alembic upgrade head
    ```
5.  **접속 확인:**
    * FastAPI Docs: `http://localhost:8000/docs`

## 🤝 기여자 및 라이선스

| **백진명** | 프로젝트 리드 개발 및 설계 | [Mikang87](https://github.com/Mikang87) |

License: <선택한 라이선스 (예: MIT License)>

---

## 💭 향후 계획 및 개선 사항

* **Frontend 개발:** React 또는 Vue를 사용하여 주문 목록 및 채널 관리 페이지 대시보드 구현.
