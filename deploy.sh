YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 현재 실행된 프로세스 중에 streamlit을 찾는다.
$CURRENT_PID=$(pgrep -fl streamlit | awk '{print $1}')

echo "${YELLOW}[INFO] Running application pid : $CURRENT_PID${NC}"

# 현재 실행된 프로세스가 있으면 종료한다.
if [ -z "$CURRENT_PID" ]; then
    echo "${YELLOW}[INFO] No exist running server.${NC}"
else
    echo "${YELLOW}[INFO] Kill running server. $CURRENT_PID${NC}"
    kill -15 $CURRENT_PID
    sleep 5
fi

# 최신 git pull을 받는다.
echo "${YELLOW}[INFO] Git pull${NC}"
git pull

# python 환경 변수 및 의존성 모듈 설치
echo "${YELLOW}[INFO] New application deploy${NC}"
source venv/bin/activate
pip install -r requirements.txt

# 서버 실행
echo "${YELLOW}[INFO] New application run${NC}"
cat /dev/null > nohup.out
nohup streamlit run index.py

$APP_URL=$(cat nohup.out | grep 'External' | awk '{print $3}')
echo "${YELLOW}[INFO] Application URL : $APP_URL${NC}"

$NEW_PID=$(pgrep -fl streamlit | awk '{print $1}')