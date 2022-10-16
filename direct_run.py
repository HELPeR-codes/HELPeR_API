from blueprints.basic_endpoints.role_config import  rconfig
nlp_role =rconfig.NLP_role
rtokenizer = rconfig.tokenizer
role_models = rconfig.role_models
from blueprints.basic_endpoints.extract_role import extract_roles

text = "hi how are you. I am good and doing fine. I also went through the same process and did my chemo"
kwdict = extract_roles(text,nlp_role,role_models,rtokenizer )
kwdict = {str(key): str(value) for key, value in kwdict.items()}
print(kwdict)
