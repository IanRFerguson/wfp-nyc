FROM python:3.10-bullseye

WORKDIR /app

COPY . .

RUN pip install -r deploy/requirements.txt

WORKDIR /app/src

EXPOSE 5000

CMD ["gunicorn", "-b", ":5000", "wsgi"]