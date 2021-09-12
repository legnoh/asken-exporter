asken_exporter
====

Prometheus exporter for [あすけん](https://www.asken.jp).

## Usage

This exporter script works for creating metrics file only.

```sh
git clone https://github.com/legnoh/asken_exporter.git && cd asken_exporter
pipenv install
pipenv shell
ASKEN_EMAIL=$YOUR_EMAIL ASKEN_PASSWORD=$YOUR_PASSWORD pipenv run main
```

Therefore, you should be hosted in other container to export metrics.

```sh
cd container
docker-compose up -d
curl -vvv http://localhost:9101/asken.prom
```

## Metrics

please check [example](./container/example/asken.prom)


## Disclaim / 免責事項

- 当スクリプトは、あすけん 本家からは非公認のものです。
  - これらを利用したことによるいかなる損害についても当方では責任を負いかねます。
- 当スクリプトはこれらのサイトに対し、負荷をかけることを目的として制作したものではありません。
  - 利用の際は常識的な範囲でのアクセス頻度に抑えてください。
- 先方に迷惑をかけない範囲での利用を強く推奨します。
