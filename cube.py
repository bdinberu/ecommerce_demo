# Cube configuration options: https://cube.dev/docs/config

from cube import config

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

# Content to Rules modifies the filter object and adds a few blank placeholders. 
# Creating a function to only return the actual filter conditions 

# def extract_applied_filters(filters):
#     """
#     Extract all actual filter conditions from a nested filter structure.
#     Returns an empty list if no real filters are applied.
    
#     Arguments:
#         filters (dict|list): Filter structure with 'and'/'or' conditions
        
#     Returns:
#         list: List of actual filter conditions
#     """
#     if isinstance(filters, list):
#         return [f for item in filters for f in extract_applied_filters(item)]
        
#     if isinstance(filters, dict):
#         if 'and' in filters or 'or' in filters:
#             key = 'and' if 'and' in filters else 'or'
#             return [f for item in filters[key] for f in extract_applied_filters(item)]
#         return [filters]
        
#     return []

# Creating a data policy that restricts queries without filters from being executed
@config('query_rewrite')
def query_rewrite(query: dict, ctx: dict) -> dict:
  # if not extract_applied_filters(query.get('filters', [])):
  if not query.get('filters', []):
    raise Exception("Queries can't be run without a filter")
  return query 