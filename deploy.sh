# 현재 실행된 프로세스 중에 streamlit을 찾는다.
$CURRENT_PID=$(pgrep -fl streamlit | awk '{print $1}')

echo "running application pid : $CURRENT_PID"

# 현재 실행된 프로세스가 있으면 종료한다.
if [ -z "$CURRENT_PID" ]; then
    echo "no exist running server."
else
    echo "> kill -15 $CURRENT_PID"
    kill -15 $CURRENT_PID
    sleep 5
fi

# 최신 git pull을 받는다.
echo "git pull"
git pull

# python 환경 변수 및 의존성 모듈 설치
echo "new application deploy"
source venv/bin/activate
pip install -r requirements.txt

# 서버 실행
echo "new application run"
nohup streamlit run index.py