FROM selenium/standalone-chromium:latest

USER root
ENV WORKDIR=/usr/src/app
WORKDIR ${WORKDIR}

ENV TZ="Asia/Tokyo"
ENV SE_CHROMEDRIVER="/usr/bin/chromedriver"
ENV DEBUGFILE_DIR="/tmp/asken-exporter"

RUN apt -y install python3 python3-pip

COPY . ${WORKDIR}

RUN pip3 install --break-system-packages -r requirements.txt
RUN mkdir -p ${DEBUGFILE_DIR}

EXPOSE 8000

ENTRYPOINT [ "./docker-entrypoint.sh" ]

CMD [ "python3", "./main.py" ]
