FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /opt/app

COPY requirements.txt requirements.txt
RUN  pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY src .

RUN ["chmod", "+x", "/opt/app/entrypoint.sh"]
CMD ["/opt/app/entrypoint.sh"]
