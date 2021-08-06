FROM python:3.9

RUN groupadd app && useradd -m kekpass -g app

ENV PYTHONUNBUFFERED=1
ENV HOME=/home/kekpass
ENV APP_HOME=/home/kekpass/web
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

COPY requirements.txt .
COPY utils utils
RUN pip install --no-cache-dir -r requirements.txt
COPY . $APP_HOME

USER kekpass

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]