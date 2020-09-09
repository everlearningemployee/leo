FROM ubuntu
RUN apt-get update -y

ENV RUN DEBIAN_FRONTEND="noninteractive" 
RUN apt-get -y install tzdata
ENV TZ=Asia/Seoul

RUN apt-get install -y python3 python3-pip
RUN pip3 install \
    PyYAML \
    requests-oauthlib

WORKDIR /leo
COPY src .
VOLUME ["/leo/order"]
# https://softwaree.tistory.com/76
ENV PYTHONIOENCODING utf-8
CMD ["python3", "Leo.py"]
