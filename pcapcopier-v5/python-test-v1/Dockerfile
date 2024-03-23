FROM alpine:latest
ENV PYTHONUNBUFFERED=1
# ADD /opt/pcaps /opt/pcaps
# RUN mkdir -p /opt/pcaps
VOLUME ["/opt/pcaps","/opt/pcaps"]
# RUN apk add --no-cache openrc bash python3 py3-pip openssh-server
RUN apk add --update --no-cache openssh bash git openssh python3 py3-pip openssh-server
RUN rc-service ssh start
RUN rc-update add ssh
RUN mkdir -p ~root/.ssh /etc/authorized_keys && chmod 700 ~root/.ssh/
RUN echo -e "Port 22\n" >> /etc/ssh/sshd_config
RUN cp -a /etc/ssh /etc/ssh.cache
RUN rm -rf /var/cache/apk/*
RUN rc-update add sshd && rc-service sshd start
RUN adduser -s /bin/bash -D -G wheel -u 1000 -g -m silentdefense
RUN echo 'silentdefense:$6$3.npOCuURBMHmyeM$ioEGACbo24W7yjqAv8HDWRAtcGFjgB3ZnYoSR8HBrl8NXyrQ2tcniZbuZgB7oXCzvhcxdOjZqlUkEe3jH3Sv61' | chpasswd -e
#USER silentdefense
WORKDIR /home/silentdefense
RUN mkdir -p /home/silentdefense/.config/pip/
ADD pip.conf /home/silentdefense/.config/pip/pip.conf
ADD pcapcopier.py /home/silentdefense/pcapcopier.py
RUN pip install pexpect --break-system-packages
RUN pip install paramiko --break-system-packages
RUN pip install scp --break-system-packages
CMD ["/bin/bash"]
#CMD ["python", "/home/silentdefense/pcapcopier.py"]
