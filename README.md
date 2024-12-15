asken-exporter
====

Prometheus exporter for [あすけん](https://www.asken.jp).

## Usage

### docker

```sh
# please fulfil your credentials
cat <<EOF > .env
ASKEN_USERNAME=youremail@localhost
ASKEN_PASSWORD=yourawesomepassword
EOF

# start
docker run -d -p 8000:8000 \
  --shm-size="2g" \
  --env-file .env \
  legnoh/asken-exporter

# option: start with debugdir mount
mkdir -p $HOME/asken-exporter
docker run -d -p 8000:8000 \
  --shm-size="2g" \
  --env-file .env \
  -v $HOME/asken-exporter:/tmp/asken-exporter \
  legnoh/asken-exporter

# wait 60s and get request
curl http://localhost:8000/metrics
```

### local

```sh
# clone
git clone https://github.com/legnoh/asken-exporter.git && cd asken-exporter
pipenv install

# please fulfil your credentials
cp example.env .env
vi .env

# execute
pipenv run main
```

## Metrics

please check [example](./example.prom)

## Disclaim / 免責事項

- 当スクリプトは、あすけん 本家からは非公認のものです。
  - これらを利用したことによるいかなる損害についても当方では責任を負いかねます。
- 当スクリプトはこれらのサイトに対し、負荷をかけることを目的として制作したものではありません。
  - 利用の際は常識的な範囲でのアクセス頻度に抑えてください。
- 先方に迷惑をかけない範囲での利用を強く推奨します。
