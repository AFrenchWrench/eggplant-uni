FROM python:3.11.4-alpine
RUN mkdir -p /home/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r $APP_HOME/requirements.txt

COPY ./entrypoint.sh $APP_HOME/entrypoint.sh
RUN chmod +x $APP_HOME/entrypoint.sh
RUN sed -i 's/\r$//' $APP_HOME/entrypoint.sh && chmod +x $APP_HOME/entrypoint.sh
RUN dos2unix $APP_HOME/entrypoint.sh

COPY . $APP_HOME

ENTRYPOINT ["/home/app/web/entrypoint.sh"]