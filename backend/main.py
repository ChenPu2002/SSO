from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
import jwt

# 定义 JWT 配置参数
JWT_SECRET = "your_jwt_secret"  # 请在生产环境中使用环境变量或更安全的方式管理
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

origins = [
"http://localhost:8080",
"http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 指定允许跨域的源
    allow_credentials=True,  # 如果前端需要传递 Cookie 或授权头，请设置为 True
    allow_methods=["*"],  # 允许所有 HTTP 方法（如 GET、POST、PUT、DELETE 等）
    allow_headers=["*"],  # 允许所有自定义头
)

# 模拟的用户数据（示例，仅作演示用途）
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "admin"  # 注意：实际项目中绝对不要明文存储密码
    }
}

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="无效凭证")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token 已过期")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token 校验失败")

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username = verify_token(token)
    return username

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"你好 {current_user}, 你已访问受保护的数据。"}

@app.get("/validatetoken")
async def validate_token(token: str):
    username = verify_token(token)
    return {"username": username}