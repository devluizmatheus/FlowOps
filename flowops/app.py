from fastapi import FastAPI

from flowops.routers import users, organizations

app = FastAPI(title='FlowOps API')

app.include_router(users.router)
app.include_router(organizations.router)


@app.get('/health')
def health_check():
    return {'status': 'ok'}