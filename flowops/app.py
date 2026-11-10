from fastapi import FastAPI

from flowops.routers import users

app = FastAPI(title='FlowOps API')

app.include_router(users.router)

@app.get('/health')
def health_check():
    return {'status': 'ok'}