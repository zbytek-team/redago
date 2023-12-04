FROM python:3.11

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY redago_backend /redago_backend

COPY redago_core /redago_core

CMD ["uvicorn", "redago_backend.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
