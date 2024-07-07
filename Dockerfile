FROM python:3.9 

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scripts/ /app/scripts/

CMD ["python", "/app/scripts/monitor.py"]