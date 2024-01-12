# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11.1-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN python -m pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv sync --system

WORKDIR /app
COPY . /app

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cmsdemo.wsgi"]
