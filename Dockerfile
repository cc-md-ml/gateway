FROM python:3.10-slim

EXPOSE 8000

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

CMD ["fastapi", "run", "app/main.py", ,"--proxy-headers", "--port", "80"]