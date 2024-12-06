# Cube configuration options: https://cube.dev/docs/config

from cube import config
import json
import os

# Semantic Layer Sync 
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


@config('context_to_app_id')
def context_mapping(ctx: dict):
  return ctx['securityContext'].setdefault('roles')


# Identifying any roles that have been assigned to the user 
@config('context_to_roles')
def context_to_roles(context):
    roles = context.get("securityContext", {}).get("roles", [])
    if roles:
        print(f"Roles found: {roles}")
    else:
        print("No roles found, returning empty list.")
    return roles


# ContentToRules modifies the filter object and adds a new 'and' dictionary 
# Determining the actual filter conditions 
def extract_matching_dicts(data):
    matching_dicts = []
    keys = ['values', 'member', 'operator']

    # Recursive function to traverse through the list or dictionary
    def traverse(element):
        if isinstance(element, dict):
            # Check if any of the specified keys are in the dictionary
            if any(key in element for key in keys):
                matching_dicts.append(element)
            # Traverse the dictionary values
            for value in element.values():
                traverse(value)
        elif isinstance(element, list):
            # Traverse the list items
            for item in element:
                traverse(item)

    traverse(data)
    return matching_dicts


# Creating a data policy that restricts queries without filters from being executed
# @config('query_rewrite')
# def query_rewrite(query: dict, ctx: dict) -> dict:
#   filters = extract_matching_dicts(query.get('filters'))
  
#   if not filters:
#     raise Exception("Queries can't be run without a filter")
#   return query 

# Validate the username and password of the user submitting the API request 
@config('check_sql_auth')
def check_sql_auth(query: dict, username: str, password: str) -> dict:
  print(security_context)
  security_context = {
    'username': username
    # , 'roles': "administrator"
  }
  print(security_context)
  return {
    'password': os.environ['CUBEJS_SQL_PASSWORD'],
    'securityContext': security_context
  }