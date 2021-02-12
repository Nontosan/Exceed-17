FROM python:3.8.5

WORKDIR /frontend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV TZ=Asia/Bangkok
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD [ "python", "./app.py" ] 