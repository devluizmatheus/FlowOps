from fastapi import FastAPI

app = FastAPI(title='FlowOps API')


@app.get('/health')
def health_check():
    return {'status': 'ok'}