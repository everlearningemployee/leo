FROM ubuntu
RUN apt update -y
RUN apt install -y python3 python3-pip
RUN pip3 install \
    PyYAML \
    requests-oauthlib

WORKDIR /leo
COPY src .
VOLUME ["/leo/order"]
# https://softwaree.tistory.com/76
ENV PYTHONIOENCODING utf-8
CMD ["python3", "Leo.py"]
