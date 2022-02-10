FROM nginx:latest

RUN apt update && apt install -y python3 python3-pip --no-install-recommends
RUN pip install flask

RUN mkdir /app /tmp/nginx
COPY app.py nginx.conf run.sh /app/
WORKDIR /app/
RUN chmod +x run.sh
CMD ["/app/run.sh"]

EXPOSE 8000
