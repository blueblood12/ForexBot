FROM python:3.10

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir forexbot

WORKDIR /forexbot

COPY requirements.txt .

RUN pip install --upgrade pip 

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "bot.py", "runserver" ]
