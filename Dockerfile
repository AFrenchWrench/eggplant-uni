FROM python:3.11.4-alpine

WORKDIR .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /command/entrypoint.sh
RUN chmod +x /command/entrypoint.sh

COPY . .

ENTRYPOINT ["/command/entrypoint.sh"]