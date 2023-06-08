FROM lscr.io/linuxserver/wireguard:latest
RUN \
	apk add --no-cache libmagic python3 py3-pip && \
	pip install kyzylborda_lib && \
	mkdir -p /etc/services.d/server
COPY server.py /
COPY start.sh /etc/services.d/server/run
COPY config /config
