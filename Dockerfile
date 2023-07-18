FROM seleniarm/standalone-chromium:latest

USER root
WORKDIR /usr/src/app

ENV DISPLAY=:99
ENV TZ="Asia/Tokyo"

RUN apt -y update \
    && apt -y install python3 python3-pip

COPY . ${WORKDIR}

RUN pip3 install --break-system-packages -r requirements.txt \
    && rm -rf requirements.txt

EXPOSE 8000

ENTRYPOINT [ "./docker-entrypoint.sh" ]

CMD [ "python3", "./main.py" ]
