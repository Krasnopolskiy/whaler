FROM python:3.9

ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/home/web
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

COPY requirements.txt .
COPY utils utils
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . $APP_HOME

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]