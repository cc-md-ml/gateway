FROM python:3.10-slim

ARG ENVIRONMENT
ARG DB_HOST
ARG DB_PORT
ARG DB_USER
ARG DB_PASSWORD
ARG DB_NAME
ARG SECRET_KEY
ARG GROQ_API_KEY

ENV ENVIRONMENT ${ENVIRONMENT}
ENV DB_HOST ${DB_HOST}
ENV DB_PORT ${DB_PORT}
ENV DB_USER ${DB_USER}
ENV DB_PASSWORD ${DB_PASSWORD}
ENV DB_NAME ${DB_NAME}
ENV SECRET_KEY ${SECRET_KEY}
ENV GROQ_API_KEY ${GROQ_API_KEY}

EXPOSE 8000

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

CMD uvicorn src.main:app --proxy-headers --reload --port 8000 --host 0.0.0.0
