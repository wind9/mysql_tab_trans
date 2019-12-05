FROM centos:latest
RUN yum install -y python3 python3-pip
RUN which python3 | xargs -i ln -s {} /usr/bin/python && which pip3 | xargs -i ln -s {} /usr/bin/pip
ADD . /python
WORKDIR /python
RUN pip install -r requirements.txt
CMD ["python", "trans.py"]