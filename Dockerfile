FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

COPY cloudfunction/ cloudfunction/

RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]