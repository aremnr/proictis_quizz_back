FROM python:3.11-slim
LABEL authors="Armen"
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "quiz_app.main:app", "--host", "0.0.0.0", "--port", "8081"]