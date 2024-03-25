FROM alpine:latest
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache bash sudo git python3 py3-pip openssh
RUN sed -i 's/^Port/#Port/g' /etc/ssh/sshd_config
RUN echo 'Port 2022' >> /etc/ssh/sshd_config
RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 2022
COPY entrypoint.sh /
RUN mkdir -p /opt/pcaps
VOLUME ["/opt/pcaps","/opt/pcaps"]
VOLUME ["/home/silentdefense","/home/silentdefense"]

RUN rm -rf /var/cache/apk/*
RUN adduser -s /bin/bash -D -G wheel -u 1000 -g -m silentdefense
RUN echo 'silentdefense:$6$3.npOCuURBMHmyeM$ioEGACbo24W7yjqAv8HDWRAtcGFjgB3ZnYoSR8HBrl8NXyrQ2tcniZbuZgB7oXCzvhcxdOjZqlUkEe3jH3Sv61' | chpasswd -e
RUN echo 'silentdefense ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers
#USER silentdefense
WORKDIR /home/silentdefense
RUN mkdir -p /home/silentdefense/.config/pip/
ADD pip.conf /home/silentdefense/.config/pip/pip.conf
ADD pcapcopier.py /home/silentdefense/pcapcopier.py
RUN pip install pexpect --break-system-packages
RUN pip install paramiko --break-system-packages
RUN pip install scp --break-system-packages
#CMD ["/bin/bash"]
#CMD ["python", "/home/silentdefense/pcapcopier.py"]
