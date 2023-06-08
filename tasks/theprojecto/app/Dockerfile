FROM imachug/kyzylborda_lib
RUN apk add --no-cache gcc musl-dev linux-headers
WORKDIR /app
COPY web /app
RUN pip install -r requirements.txt
CMD ["python", "server.py", "/tmp/app.sock"]
