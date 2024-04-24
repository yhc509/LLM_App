import mysql.connector as msc

# MySQL 서버 연결 정보
_host = 'mydatabase.c9qe4wygwsw5.ap-northeast-2.rds.amazonaws.com'
_database = 'TestDB'
_table = 'NewTable'
_user = ''
_password = ''

# MySQL 서버에 연결
conn = msc.connect(host = _host, database = _database, user=_user, password=_password)

# 커서 생성
cursor = conn.cursor()

# 데이터 삽입 쿼리 작성
query = f"INSERT INTO {_database}.{_table} VALUES (%s, %s, %s)"

# 삽입할 데이터 지정
data = ('홍길동', 1, 'key_12345')

# 쿼리 실행
cursor.execute(query, data)

# 변경 사항 커밋
conn.commit()

# 연결 종료
conn.close()