# Cube configuration options: https://cube.dev/docs/config

from cube import config
import json
import os


# def get_user_name(context):
#   user_name = False
#   if not roles:
#     user_name = context.get("securityContext", {}).get("cubeCloud", {}).get("username", False)
#     if not user_name:
#       user_name = context.get("securityContext", {}).get("user_name", False)
#     if user_name:
#       print(f"context_to_roles: User found: {user_name}")
#   return user_name

def get_roles(context):
  roles = context.get("securityContext", {}).get("cubeCloud", {}).get("roles", [])
  user_name = False
  if not roles:
    user_name = context.get("securityContext", {}).get("cubeCloud", {}).get("username", False)
    if not user_name:
      user_name = context.get("securityContext", {}).get("user_name", False)
    if user_name:
      print(f"context_to_roles: User found: {user_name}")
      # Perform a user lookup to your identity provider (e.g. LDAP)
      # e.g. roles = get_roles(username)
  if roles:
      print(f"Roles found: {roles}")
  # check for admin account
  elif user_name and user_name == 'cube':
    roles = ['admin']
    print(f"Roles: {roles}")
  else:
    print("No roles found, returning default role")
    return ['default']
  return roles

# Semantic Layer Sync 
@config('semantic_layer_sync')
def sls(ctx: dict) -> list:
    return [{
  "type": "tableau-cloud",
  "name": "Tableau Cloud Sync",
  "useRlsFilters": True,
  "config": {
    "database": "Cube Cloud: bd_ecomm_demo",
    "personalAccessToken": "ecomm_demo_bd",
    "personalAccessTokenSecret": "CaSfFFyOR3mj1ncwLQHAww==:8jUMFFHdlhXSdcbdH6VZFzxHfQKZPsrL",
    "region": "us-west-2b",
    "site": "cubedev"
  }
}]

@config('context_to_api_scopes')
def context_to_api_scopes(ctx: dict, default_scopes: list[str]) -> list[str]:
  if ctx.get('service', False):
    return ["jobs"] + default_scopes
  return default_scopes

@config('context_to_app_id')
def context_to_app_id(ctx: dict):
  roles = get_roles(ctx)
  user_name = False
  app_id = '_'.join(sorted(roles))
  state = ctx.get("securityContext", {}).get("state", False)
  if state:
    app_id += '_' + state
  print(f"app_id: {app_id}")
  return app_id


# Identifying any roles that have been assigned to the user 
@config('context_to_roles')
def context_to_roles(context):
  security_context = context.get("securityContext", {})
  print(f"context to roles: {security_context}")

  roles = get_roles(context)
  return roles


# Creating a data policy that injects a user filter
@config('query_rewrite')
def query_rewrite(query: dict, ctx: dict) -> dict:
  context = ctx['securityContext']
  print(f'query_rewrite {context}')
  print(f'query pre-rewrite: {query}')
  # Cube user is service account
  # if 'user_name' in context and context['user_name'] != 'cube':
  #   query['filters'].append({
  #     'member': 'users.state',
  #     'operator': 'equals',
  #     'values': [context.get('state', 'us-ca')]
  #   })
  #   pass
  return query 

# Validate the username and password of the user submitting the API request 
@config('check_sql_auth')
def check_sql_auth(query: dict, username: str, password: str) -> dict:
  # Perform a user lookup to your identity provider (e.g. LDAP)
  # When username is different than the service account like 'cube'
  # e.g. get_security_context(username)
  security_context = {
    'user_name': username,
    'state': 'us-ca'
  }

  print(f'check_sql_auth: {security_context}')
  
  return {
    'password': os.environ['CUBEJS_SQL_PASSWORD'],
    'securityContext': security_context
  }

@config('can_switch_sql_user')
def can_switch_sql_user(current_user: str, new_user: str) -> dict:
 
  return True