FROM python:3.11-alpine AS builder

WORKDIR /tmp
COPY ./pyproject.toml ./poetry.lock ./

RUN pip install poetry==1.7.1 && \
    poetry export -n --without dev -f requirements.txt -o requirements.txt

FROM python:3.11-alpine

WORKDIR /app

COPY --from=builder /tmp/requirements.txt ./
COPY ./project/ ./project/

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app

ENTRYPOINT ["/usr/local/bin/python", "/app/project/main.py"]
CMD ["--help"]
