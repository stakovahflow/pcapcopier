FROM alpine:latest
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache bash sudo git python3 py3-pip openssh curl
RUN sed -i 's/^Port/#Port/g' /etc/ssh/sshd_config
RUN echo 'Port 2022' >> /etc/ssh/sshd_config
RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 2022
ADD entrypoint.sh /
ADD pcapcopier.py /opt/pcapcopier/bin/pcapcopier.py
ADD pcapcopier-banner.txt /etc/motd
RUN mkdir -p /opt/pcaps
RUN mkdir -p /var/log/pcapcopier
RUN mkdir -p /root/.ssh
RUN touch /root/.ssh/known_hosts
RUN echo '* * * * * date >> /home/silentdefense/cron.log 2>&1' >> /etc/crontabs/root
RUN rm -rf /var/cache/apk/*
RUN adduser -s /bin/bash -D -G root -u 1000 -g -m silentdefense
RUN echo 'silentdefense:$6$3.npOCuURBMHmyeM$ioEGACbo24W7yjqAv8HDWRAtcGFjgB3ZnYoSR8HBrl8NXyrQ2tcniZbuZgB7oXCzvhcxdOjZqlUkEe3jH3Sv61' | chpasswd -e
RUN echo 'silentdefense ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN mkdir -p /opt/pcapcopier/bin
WORKDIR /opt/pcapcopier/bin
RUN pip install pexpect --break-system-packages
RUN pip install paramiko --break-system-packages
RUN pip install scp --break-system-packages


