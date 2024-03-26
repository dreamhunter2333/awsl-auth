FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt /requirements.txt
RUN python3 -m pip install -r /requirements.txt
COPY . /app
EXPOSE 8000
ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
