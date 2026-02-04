# Azure Web App 배포 가이드

## 배포 방법

### 1. Azure Portal에서 Web App 생성
1. Azure Portal (https://portal.azure.com) 접속
2. "Web App" 생성
3. 설정:
   - Runtime stack: **Python 3.12**
   - Operating System: **Linux**
   - Region: 가까운 지역 선택 (예: Korea Central)

### 2. 환경 변수 설정
Azure Portal > Web App > Configuration > Application Settings에 추가:

```
NEO4J_URI=neo4j+s://761c1872.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=<your-password>
NEO4J_DATABASE=neo4j
```

### 3. 배포 방법 옵션

#### 옵션 A: GitHub 연동 (권장)
1. Azure Portal > Deployment Center
2. Source: **GitHub** 선택
3. Repository: `jaehoyangkorea/yang_neo4j_cost_02_lges`
4. Branch: `main`
5. 자동 배포 설정

#### 옵션 B: ZIP 배포
1. 프로젝트 루트에서 ZIP 파일 생성 (아래 명령어 참조)
2. Azure Portal > Deployment Center > FTPS credentials 확인
3. Kudu (https://<your-app-name>.scm.azurewebsites.net) 접속
4. Tools > Zip Push Deploy에서 ZIP 업로드

```bash
# ZIP 파일 생성
zip -r deploy.zip . -x "*.git*" -x "*__pycache__*" -x "*.pyc" -x ".env*"
```

#### 옵션 C: Azure CLI
```bash
# Azure CLI 로그인
az login

# Web App에 배포
az webapp up --name <your-app-name> --resource-group <your-rg> --runtime "PYTHON:3.12"
```

### 4. 시작 명령어 설정
Azure Portal > Configuration > General Settings:

**Startup Command:**
```
bash startup.sh
```

또는 직접:
```
gunicorn --bind=0.0.0.0:8000 --chdir visualization --timeout 600 graph_api_server:app
```

### 5. 포트 설정
Azure는 기본적으로 `PORT` 환경 변수를 제공합니다.

`visualization/graph_api_server.py`에서:
```python
port = int(os.getenv('PORT', 8000))
app.run(host='0.0.0.0', port=port)
```

### 6. 배포 후 확인
- URL: `https://<your-app-name>.azurewebsites.net`
- 로그 확인: Azure Portal > Log stream

## 필수 파일
- `requirements.txt` - Python 패키지
- `runtime.txt` - Python 버전
- `startup.sh` - 시작 스크립트
- `.env` 파일은 업로드하지 말고 Azure Configuration에서 설정

## 주의사항
1. `.env` 파일은 절대 업로드하지 마세요 (보안)
2. Neo4j URI, 비밀번호는 Azure Configuration에서 설정
3. 첫 배포 후 로그를 확인하여 오류 체크
4. 데이터는 이미 Neo4j에 업로드되어 있어야 함

## 트러블슈팅
- **502 Bad Gateway**: 로그 확인, 시작 명령어 및 포트 설정 확인
- **500 Error**: Neo4j 연결 정보 확인
- **앱이 시작 안 됨**: `requirements.txt` 및 `startup.sh` 권한 확인
