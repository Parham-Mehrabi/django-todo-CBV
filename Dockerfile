FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# add secret key and other api keys here to avoid hard codding them
ENV SECRET_KEY django-insecure-#s04_bzd3_v0h7^3))%nzru%o#x-$ruv!uk+rat8n@@_+_(zf(

# set proxy because pip is not avalible in my country
# ENV HTTPS_PROXY=http://172.18.0.1:8118
# ENV ALL_PROXY=http://172.18.0.1:8118

# ENV HTTPS_PROXY=http://192.168.101.209:10809
# ENV ALL_PROXY=http://192.168.101.209:10809

WORKDIR /app

COPY requirments.txt /app/

COPY ./backend /app/

RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirments.txt

# unset proxy after install the packages
RUN unset HTTPS_PROXY
RUN unset ALL_PROXY

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
