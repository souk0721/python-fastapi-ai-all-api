
from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from packages.fastapi_mo.routers_mo.route_user import router as route_user
from packages.fastapi_mo.routers_mo.route_video import router as route_video
from packages.fastapi_mo.routers_mo.route_ai import router as route_ai
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(route_user)
app.include_router(route_video)
app.include_router(route_ai)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# @app.get("/static/{file_path:path}", dependencies=[Depends(get_current_user)])
# async def read_static_file(file_path: str):
#     return StaticFiles(directory="static")

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0",reload=True, port=8001)
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8001)