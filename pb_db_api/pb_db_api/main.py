from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from pb_db_api.db import SessionLocal
from pb_db_api.routes import routes

app = FastAPI()


@app.middleware('http')
def db_session_middleware(request: Request, call_next):
    response = Response('Internal server error', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = call_next(request)
    finally:
        request.state.db.close()
    return response


app.include_router(routes)
