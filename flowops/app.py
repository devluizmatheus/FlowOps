from fastapi import FastAPI

from flowops.routers import users, organizations, organizational_structure

app = FastAPI(title='FlowOps API')

app.include_router(users.router)
app.include_router(organizations.router)
app.include_router(organizational_structure.router)


@app.get('/health')
def health_check():
    return {'status': 'ok'}