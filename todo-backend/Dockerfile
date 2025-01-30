FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install flask psycopg2-binary
EXPOSE 5000
CMD [ "python3", "todo-backend.py" ]