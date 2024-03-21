FROM python:3.12
ADD pcapcopier.py .
RUN pip install pexpect
RUN pip install paramiko
RUN pip install scp
CMD ["python", "./pcapcopier.py"]
