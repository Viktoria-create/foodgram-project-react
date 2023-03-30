#FROM python:3.7-slim
#WORKDIR /app
#RUN python -m pip install --upgrade pip
#COPY requirements.txt .
#RUN pip3 install -r requirements.txt --no-cache-dir
#COPY . .
#CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0.0.0.0:8000" ]

FROM python:3.7
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir
COPY backend/ ./
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0.0.0.0:8000" ]
