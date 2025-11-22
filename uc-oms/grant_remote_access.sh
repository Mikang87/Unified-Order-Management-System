#!/bin/bash
# 파일: grant_remote_access.sh

# ... (기존 대기 로직)
echo "Waiting for MySQL to start..."
until mysql -u root -p"$MYSQL_ROOT_PASSWORD" -h localhost -e "SELECT 1;" > /dev/null 2>&1; do
  sleep 1
done
echo "MySQL is ready."


# 2. 환경 변수를 사용하여 동적 SQL 명령 실행 (수정된 부분)
mysql -u root -p"$MYSQL_ROOT_PASSWORD" -h localhost "$MYSQL_DATABASE" <<EOF
# 모든 호스트 (%)에서 접속 가능하도록 인증 방식을 mysql_native_password로 변경합니다.
ALTER USER '$MYSQL_USER'@'%' IDENTIFIED WITH mysql_native_password BY '$MYSQL_PASSWORD';

# 해당 사용자에게 데이터베이스에 대한 모든 권한을 부여합니다.
GRANT ALL PRIVILEGES ON $MYSQL_DATABASE.* TO '$MYSQL_USER'@'%';

FLUSH PRIVILEGES;
EOF

echo "✅ Remote access granted and authentication method updated for user $MYSQL_USER."
