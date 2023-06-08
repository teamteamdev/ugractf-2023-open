FROM python:3-alpine
RUN apk add --no-cache gcc musl-dev linux-headers unzip && pip install gunicorn
COPY . /home/bookkeeper/books
WORKDIR /home/bookkeeper/books
RUN adduser -S bookkeeper && chown -R bookkeeper /home/bookkeeper
USER bookkeeper
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn", "-b", "unix:/tmp/app.sock", "server:make_app()"]
