FROM python:3.7
WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app"
COPY config.json /etc/config.json
COPY . .
RUN pip install gunicorn
RUN pip install -r Requirements.txt
ENV PORT=8080
EXPOSE $PORT
CMD exec gunicorn --bind :$PORT -w 1 --threads 8 run:app
