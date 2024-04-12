FROM python:3.11.4-alpine
RUN mkdir -p /home/app

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

# copy entrypoint.sh
COPY ./entrypoint.sh /command/
RUN sed -i 's/\r$//g' /command/entrypoint.sh
RUN chmod +x /command/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/command/entrypoint.sh"]