from cube import TemplateContext
 
template = TemplateContext()

# Validating whether the user is assigned a 'trusted' role
# Creating a rule to only display unmasked data to 'trusted' roles 
@template.function('masked')
def masked(sql, security_context):
  trusted_roles = ['leadership', 'executive']
  role_check = False 

  # print("masked check")
  # print(security_context["cubeCloud"])

  if 'cubeCloud' in security_context and security_context["cubeCloud"].setdefault('roles') is not None:
    for role in security_context["cubeCloud"].setdefault('roles'):
      if role in trusted_roles:
        role_check = True 

  if role_check:
    return sql
  else:
    return "'--- masked ---'"
