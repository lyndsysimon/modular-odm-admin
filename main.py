from flask import Flask, request
import models
from modularodm.fields import Field
import json

app = Flask(__name__)

from mako.lookup import TemplateLookup

makolookup = TemplateLookup(directories=['templates'])

def render(filename, **kwargs):
    t = makolookup.get_template(filename).render(**kwargs)
    return t

def get_schema_keys(schema_name):
    schema = models.StoredObject._collections[schema_name]
    schema_keys = {k:v.__class__.__name__ for k,v in schema.__dict__.iteritems() if isinstance(v, Field)}
    return schema_keys

@app.route('/')
def index():
    schemas = models.StoredObject._collections
    return render(
        filename="index.mako",
        schemas=schemas)

@app.route('/<schema_name>')
def schema_obj(schema_name):
    schema_obj = models.StoredObject._collections[schema_name]
    info = json.dumps(get_schema_keys(schema_name))
    data = schema_obj.find_all()
    entries = []
    for i in list(data):
        entries.append(i.to_storage())
    return render(
        filename="schema_obj.mako",
        title=schema_name,
        info=info,
        entries=entries,
        primary_name=schema_obj._primary_name
    )

@app.route('/<schema_name>/<sid>/edit', methods=['GET', 'POST'])
def edit(schema_name, sid):
    schema_obj = models.StoredObject._collections[schema_name]
    saved_obj = schema_obj.load(sid)
    json_data = saved_obj.to_storage()
    for key, obj in saved_obj._fields.iteritems():
        if obj.__class__.__name__ == 'ForeignField':
            del json_data[key]


    if request.method == 'POST':
        for key in json_data.keys():
            if key in request.form:
                setattr(saved_obj, key, request.form[key])
                # data[key]=request.form[key]

        # schema_obj(**data).save()
        saved_obj.save()
    return render(
        filename="edit.mako",
        type=schema_name,
        data=json_data
    )

if __name__ == '__main__':
    app.run(debug=True)
