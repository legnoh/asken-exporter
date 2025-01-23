FROM selenium/standalone-chromium:latest
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

USER root
ENV WORKDIR=/usr/src/app
WORKDIR ${WORKDIR}

ENV TZ="Asia/Tokyo"
ENV SE_CHROMEDRIVER="/usr/bin/chromedriver"
ENV DEBUGFILE_DIR="/tmp/asken-exporter"

COPY . ${WORKDIR}

RUN uv sync --frozen
RUN mkdir -p ${DEBUGFILE_DIR}

EXPOSE 8000

CMD ["uv", "run", "main.py"]
