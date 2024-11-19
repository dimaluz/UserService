FROM python:3.11-slim

COPY requirements.txt /temp/requirements.txt
COPY user_service /user_service
WORKDIR /user_service

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

RUN apt-get update && apt-get install -y \
gcc \
libpq-dev \
&& rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r /temp/requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]