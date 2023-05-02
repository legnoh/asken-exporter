FROM seleniarm/standalone-chromium:latest

USER root
WORKDIR /usr/src/app

ARG PYTHON_VERSION="3.10.0"
ENV DISPLAY=:99
ENV TZ="Asia/Tokyo"

RUN apt -y update \
    && apt -y install build-essential libreadline-dev libncursesw5-dev \
                      libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev \
                      libbz2-dev libffi-dev xvfb wget zlib1g-dev \
    && wget -c https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz \
    && tar -Jxvf Python-${PYTHON_VERSION}.tar.xz \
    && cd Python-${PYTHON_VERSION} \
    && ./configure --enable-optimizations \
    && make altinstall \
    && python3 --version \
    && apt -y install python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /usr/src/app/Python-${PYTHON_VERSION}*

COPY . ${WORKDIR}

RUN pip3 install --break-system-packages -r requirements.txt \
    && rm -rf requirements.txt

EXPOSE 8000

ENTRYPOINT [ "./docker-entrypoint.sh" ]

CMD [ "python3", "./main.py" ]
