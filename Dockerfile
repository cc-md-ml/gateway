FROM python:3.10-slim

ARG ENVIRONMENT
ARG DB_PASSWORD
ARG DB_URL
ARG DB_USERNAME
ARG SECRET_KEY

ENV ENVIRONMENT ${ENVIRONMENT}
ENV DB_PASSWORD ${DB_PASSWORD}
ENV DB_URL ${DB_URL}
ENV DB_USERNAME ${DB_USERNAME}
ENV SECRET_KEY ${SECRET_KEY}

EXPOSE 8000

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

CMD ["fastapi", "run", "app/main.py", ,"--proxy-headers", "--port", "8000"]