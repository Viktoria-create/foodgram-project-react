#FROM python:3.7-slim
#WORKDIR /app
#RUN python -m pip install --upgrade pip
#COPY requirements.txt .
#RUN pip3 install -r requirements.txt --no-cache-dir
#COPY . .
#CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0.0.0.0:8000" ]

# FROM python:3.11-slim

# WORKDIR /app

# RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y \
#        libpango1.0-dev \
#        libglib2.0-dev && \
#   apt-get clean && \
#    rm -rf /var/lib/apt/lists/*

# COPY requirements.txt ./

# RUN pip3 install -r requirements.txt --no-cache-dir

# COPY . .

# ENV PYTHONUNBUFFERED=1 \
#    PYTHONDONTWRITEBYTECODE=1

# CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000" ]

FROM python:3.7
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0.0.0.0:8000" ]
