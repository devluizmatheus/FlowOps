FROM python:3.14-slim

WORKDIR /flowops

RUN pip install --no-cache-dir "poetry>=2,<3"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root --no-interaction --no-ansi

COPY flowops/ ./flowops/

EXPOSE 8000

CMD ["fastapi", "run", "flowops/app.py", "--host", "0.0.0.0", "--port", "8080"]