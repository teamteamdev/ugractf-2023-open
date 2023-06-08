FROM imachug/kyzylborda_lib
RUN \
	apk add --no-cache openssh-server && \
	addgroup user && \
	adduser -s /sbin/login.py user -G user -D && \
	echo -e 'wohpheu0Vei\nwohpheu0Vei' | passwd user && \
	mkdir /home/user/.ssh && \
	chown user:user /home/user/.ssh && \
	chmod 700 /home/user/.ssh && \
	echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFyG5dOjpTGk3x69/ikMkKAcgMNErdt3zslQ1OiHBhdc defaultuser@localhost' >> /home/user/.ssh/authorized_keys && \
	chown user:user /home/user/.ssh/authorized_keys && \
	chmod 600 /home/user/.ssh/authorized_keys && \
	ssh-keygen -A && \
	echo 'AcceptEnv AUTH' >> /etc/ssh/sshd_config && \
	echo 'PasswordAuthentication no' >> /etc/ssh/sshd_config && \
	echo 'Port 18602' >> /etc/ssh/sshd_config
COPY login.py /sbin/login.py
CMD ["/usr/sbin/sshd", "-D", "-e"]
