FROM python:3.8.5

WORKDIR /frontend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ] 