FROM python:3.11-slim
ARG REMOTE_SELENIUM_ADDRESS
ARG SELENIUM_REQUESTS_PROXY_HOST
ENV REMOTE_SELENIUM_ADDRESS=$REMOTE_SELENIUM_ADDRESS
ENV SELENIUM_REQUESTS_PROXY_HOST=$SELENIUM_REQUESTS_PROXY_HOST

WORKDIR app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
CMD poetry run uvicorn --host 0.0.0.0 letterboxd_collage.app:app