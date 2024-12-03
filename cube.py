# Cube configuration options: https://cube.dev/docs/config

from cube import config


@config('semantic_layer_sync')
def sls(ctx: dict) -> list:
    return [{
  "type": "tableau-cloud",
  "name": "Tableau Cloud Sync",
  "config": {
    "database": "Cube Cloud: ecomm_bd",
    "personalAccessToken": "ecomm_demo_bd",
    "personalAccessTokenSecret": "CaSfFFyOR3mj1ncwLQHAww==:8jUMFFHdlhXSdcbdH6VZFzxHfQKZPsrL",
    "region": "us-west-2b",
    "site": "cubedev"
  }
}]