FROM python:alpine

RUN pip install --upgrade pip

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

CMD ["python", "main.py"]