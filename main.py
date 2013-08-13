#TODO backref popovers

from flask import Flask, request, jsonify, render_template
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

@app.route('/', methods=['GET', 'POST'])
def index():
    schemas = models.StoredObject._collections
    return render(
        filename="index.mako",
        schemas=schemas)

@app.route('/<schema_name>/')
def schema_display(schema_name):
    schema_obj = models.StoredObject._collections[schema_name]
    primary_name = schema_obj._primary_name
    schema_info = json.dumps(get_schema_keys(schema_name))
    schema_entries = schema_obj.find_all()
    entry_data = []
    for i in list(schema_entries):
        storage = i.to_storage()
        ordered = OrderedDict()
        ordered[primary_name] = storage[primary_name]
        for key, value in storage.iteritems():
            if key is not primary_name and key is not "_backrefs":
                ordered[key]=value
        ordered[""] = "<a href='/{title}/{object}/edit'>edit</a>".format(title=schema_name, object=storage[primary_name])
        entry_data.append(ordered)
    return render(
        filename="schema_obj.mako",
        title=schema_name,
        schema_info=schema_info,
        schema_entries=entry_data
    )

@app.route('/<schema_name>/<sid>/')
def view_as_json(schema_name, sid):
    schema_class = models.StoredObject._collections[schema_name]
    schema_obj = schema_class.load(sid)
    json_data = schema_obj.to_storage()
    return jsonify(json_data)

@app.route('/<schema_name>/<sid>/edit', methods=['GET', 'POST'])
def edit(schema_name, sid):
    schema_class = models.StoredObject._collections[schema_name]
    schema_obj = schema_class.load(sid)
    data_dict = schema_obj.to_storage()
    message=""

    if request.method == 'POST':
        for key in data_dict.keys():
            if key in json.loads(request.form['json_data']) and key is not "_backrefs":
                incoming_data = json.loads(request.form['json_data'])
                field_type = type(schema_obj._fields[key]).__name__
                if field_type is 'BooleanField':
                    new_value = incoming_data[key]
                    if new_value == 'True':
                        new_value = True
                    else:
                        new_value = False
                elif field_type is 'IntegerField':
                    new_value = int(incoming_data[key])
                elif field_type is 'FloatField':
                    new_value = float(incoming_data[key])
                elif field_type is 'ListField':
                    base_field_type = type(schema_obj._fields[key]._field_instance).__name__
                    if base_field_type is 'BooleanField':
                        new_value = str(incoming_data[key]).split(',')
                        for i in new_value:
                            if i == 'True':
                                i = True
                            else:
                                i = False
                    elif base_field_type is 'IntegerField':
                        new_value = int(str(incoming_data[key]).split(','))
                    elif base_field_type is 'FloatField':
                        new_value = float(str(incoming_data[key]).split(','))
                    # elif base_field_type is 'DictionaryField':
                    #     (incoming_data[key])
                    # elif base_field_type is 'DateTimeField':
                    #     (incoming_data[key])
                    elif base_field_type is 'StringField':
                        new_value = str(incoming_data[key]).split(',')

                # elif field_type is 'DictionaryField':
                #     (incoming_data[key])
                # elif field_type is 'DateTimeField':
                #     (incoming_data[key])
                elif field_type is 'StringField':
                    new_value = str(incoming_data[key])
                else:
                    foreign_class = schema_obj._fields[key].base_class
                    old_value = getattr(schema_obj, key)
                    try:
                        foreign_obj = foreign_class.load(incoming_data[key])
                    except KeyError:
                        print "No object with that name"

                    if schema_obj._fields[key]._list:
                        foreign_obj = [foreign_obj]

                    if old_value != foreign_obj:
                        new_value = foreign_obj

                setattr(schema_obj, key, new_value)

        schema_obj.save()
        data_dict = schema_obj.to_storage()
        message="Edit was successful!"

    for key, value in schema_obj._fields.iteritems():
        if value.__class__.__name__ == 'ForeignField':
            foreign_key_dict = {}
            # foreign_obj = models.StoredObject._collections[key]
            foreign_obj = getattr(schema_obj, key)
            foreign_key_dict['foreign'] = True
            foreign_key_dict['schema_name'] = foreign_obj._name
            foreign_key_dict['foreign_obj'] = json.dumps(foreign_obj.to_storage())
            foreign_key_dict['primary_value'] = foreign_obj.to_storage()[foreign_obj._primary_name]
            data_dict[key] = foreign_key_dict
        if value.__class__.__name__ == 'ListField':
            if value._field_instance.__class__.__name__ == 'ForeignField':
                new_data = []
                for foreign_obj in getattr(schema_obj, key):
                    foreign_key_dict={}
                    foreign_key_dict['foreign'] = True
                    foreign_key_dict['schema_name'] = foreign_obj._name
                    foreign_key_dict['foreign_obj'] = json.dumps(foreign_obj.to_storage())
                    foreign_key_dict['primary_value'] = foreign_obj.to_storage()[foreign_obj._primary_name]
                    new_data.append(foreign_key_dict)
                data_dict[key]=new_data

                # if type(value._field_instance).__name__ == 'ForeignField'
        #     print type(value._field_instance).__name__

    # for key, value in schema_obj._fields.iteritems():
    #     if value.__class__.__name__ == 'ForeignField' or value.__class__.__name__ == 'ListField':
    #         data_dict[key]={'foreign': True, 'foreign_obj': data_dict[key]}

    return render(
        filename="edit.mako",
        schema_name=schema_name,
        schema_obj_data=data_dict,
        json_data=json.dumps(data_dict),
        schema_primary_name=schema_class._primary_name,
        message=message
    )

if __name__ == '__main__':
    app.run(debug=True)
