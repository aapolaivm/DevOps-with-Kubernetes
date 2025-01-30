FROM python:3.12-slim

WORKDIR /app

COPY create_todo.py .

RUN pip install requests

CMD ["python", "create_todo.py"]