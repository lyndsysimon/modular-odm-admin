from flask import Flask, request
import models
from modularodm.fields import Field
from collections import OrderedDict
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

@app.route('/<schema_name>/')
def schema_obj(schema_name):
    schema_obj = models.StoredObject._collections[schema_name]
    primary_name = schema_obj._primary_name
    info = json.dumps(get_schema_keys(schema_name))
    data = schema_obj.find_all()
    entries = []
    for i in list(data):
        storage = i.to_storage()
        ordered = OrderedDict()
        ordered['primary_name'] = storage[primary_name]
        for key, value in storage.iteritems():
            if key is not primary_name:
                ordered[key]=value
        ordered[""] = "<a href='/{title}/{object}/edit'>edit</a>".format(title=schema_name, object=storage[primary_name])
        entries.append(ordered)
    return render(
        filename="schema_obj.mako",
        title=schema_name,
        info=info,
        entries=entries,
        primary_name=primary_name
    )

@app.route('/<schema_name>/<sid>/edit', methods=['GET', 'POST'])
def edit(schema_name, sid):
    schema_obj = models.StoredObject._collections[schema_name]
    saved_obj = schema_obj.load(sid)
    json_data = saved_obj.to_storage()
    # for key, obj in saved_obj._fields.iteritems():
    #     if obj.__class__.__name__ == 'ForeignField':
    #         foreign_key_dict = {}
    #         m = models.StoredObject._collections[key]
    #         foreign_key_dict['foreign'] = True
    #         foreign_key_dict['object'] = getattr(saved_obj, key)
    #         foreign_key_dict['primary_value'] = m.load(json_data[key]).to_storage()[m._primary_name]
    #         json_data[key] = foreign_key_dict
    #     print obj.__class__.__name__
    #     if obj.__class__.__name__ == 'ListField':
    #         print 'deleted'
    #         del json_data[key]
    for key, obj in saved_obj._fields.iteritems():
        if obj.__class__.__name__ == 'ForeignField' or obj.__class__.__name__ == 'ListField':
            json_data[key]={'foreign': True, 'value': json_data[key]}

        # if obj.__class__.__name__ == 'ListField':
        #     print 'deleted'
        #     del json_data[key]


    if request.method == 'POST':
        for key in json_data.keys():
            if key in request.form:
                if 'foreign' in json_data[key]:
                    # foreign_schema_name = getattr(saved_obj, key)._name
                    field = saved_obj._fields[key]
                    # if field._list:
                    #     # split key by comma?
                    foreign_class = saved_obj._fields[key].base_class
                    check = getattr(saved_obj, key)
                    try:
                        object = foreign_class.load(request.form[key])
                    except KeyError:
                        object = check
                        print "No object with that name"

                    if saved_obj._fields[key]._list:
                        object = [object]

                    if key == 'tags':
                        print 'uh oh'
                    if check != object:
                        setattr(saved_obj, key, object)


                    # object.update(object._primary_name, request.form[key])
                    # object.save()
                else:
                    setattr(saved_obj, key, request.form[key])

        saved_obj.save()
    json_data = saved_obj.to_storage()
    return render(
        filename="edit.mako",
        schema_type=schema_name,
        data=json_data,
        primary_name=schema_obj._primary_name
    )

if __name__ == '__main__':
    app.run(debug=True)
