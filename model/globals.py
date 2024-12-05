from cube import TemplateContext
 
template = TemplateContext()
 
@template.function('masked')
def masked(sql, security_context):
  trusted_roles = ['administrator', 'executive']
  role_check = False 

  if security_context.setdefault('roles') is not None:
    for role in security_context.setdefault('roles'):
      if role in trusted_roles:
        role_check = True 

  if role_check:
    return sql
  else:
    return "'--- masked ---'"
