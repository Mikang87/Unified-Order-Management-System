FROM python:3.14-slim

WORKDIR /usr/src/app

# 시스템 종속성 설치 (MySQL 클라이언트 등)
# NOTE: mysqlclient 대신 psycopg2-binary 등을 사용하면 이 부분이 달라짐.
RUN apt-get update && apt-get install -y default-libmysqlclient-dev pkg-config gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /usr/src/app/app

# uvicorn으로 main.py의 app 객체를 실행합니다.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]