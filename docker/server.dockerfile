FROM python:3.8
RUN pip install pipenv
WORKDIR /app
COPY Pipfile Pipfile
RUN pipenv install --skip-lock