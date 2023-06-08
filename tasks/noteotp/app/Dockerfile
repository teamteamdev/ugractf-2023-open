FROM golang:alpine

RUN apk add fortune

WORKDIR /build
ADD go.mod .
COPY . .
RUN go build -o noteotp .

COPY ./diary /build/diary
RUN strfile diary
COPY ./flags /build/flags
RUN strfile flags

ENV FORTUNE_ARGS="7% flags 58% diary 25% zippy 10% recipes"

CMD ["/build/noteotp"]
