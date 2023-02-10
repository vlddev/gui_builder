import model
import json
from string import Template
from jinja2 import Environment, FileSystemLoader

destDir = "../generated_app/"

padding = "    "

def generateDao(model: model.Model):
    print("Generate DAO")
    env = Environment(loader=FileSystemLoader("./"))
    template = env.get_template("dao_py.jinja")
    return template.render(tablelist=model.tables.values())

def generateDbOps(model: model.Model):
    print("Generate DB operations")
    env = Environment(loader=FileSystemLoader("./"))
    template = env.get_template("db_util_py.jinja")
    return template.render(tablelist=model.tables.values())

def generateForms(model):
    print("Generate DB forms")
    env = Environment(loader=FileSystemLoader("./"))
    template = env.get_template("ui_app_py.jinja")
    return template.render(form=model.forms[0], model=model)

with open('model.json') as f:
    modelJson = json.load(f)

model = model.Model(modelJson)

with open(destDir+'dao.py', 'w') as f:
    f.write(generateDao(model))

with open(destDir+'db_util.py', 'w') as f:
    f.write(generateDbOps(model))

with open(destDir+'ui_app.py', 'w') as f:
    f.write(generateForms(model))
