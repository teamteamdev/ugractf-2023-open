FROM imachug/kyzylborda_lib
RUN apk add --no-cache gcc musl-dev linux-headers
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["./wait-for-it.sh", "-t", "30", "database:3306", "--", "gunicorn", "-b", "unix:/tmp/app.sock", "server:make_app()"]