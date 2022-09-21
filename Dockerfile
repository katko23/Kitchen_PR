FROM python:alpine

WORKDIR /app

COPY . .

EXPOSE 27003 27004

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD [ "python", "main.py"]