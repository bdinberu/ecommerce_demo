# Cube configuration options: https://cube.dev/docs/config

from cube import config


@config('semantic_layer_sync')
def sls(ctx: dict) -> list:
    return [{
  "type": "tableau-cloud",
  "name": "Tableau Cloud Sync",
  "config": {
    "database": "Cube Cloud: bd_ecomm_demo",
    "personalAccessToken": "ecomm_demo_bd",
    "personalAccessTokenSecret": "CaSfFFyOR3mj1ncwLQHAww==:8jUMFFHdlhXSdcbdH6VZFzxHfQKZPsrL",
    "region": "us-west-2b",
    "site": "cubedev"
  }
}]
 
@config('query_rewrite')
def query_rewrite(query: dict, ctx: dict) -> dict:
  
  if not query.get('filters', []):
    raise Exception("Queries can't be run without a filter")
  return query 

@config('context_to_roles')
def context_to_roles(context):
    roles = context.get("securityContext", {}).get("roles", [])
    if roles:
        print(f"Roles found: {roles}")
    else:
        print("No roles found, returning empty list.")
    return roles
