from flask_restful import fields

from app.fields.search import meta_field

node_field = {
    "id": fields.Integer,
    "project_id": fields.Integer,
    "node_type": fields.String,
    "input_shape": fields.Raw,
    "output_shape": fields.Raw,
    "in_edges": fields.List(fields.Integer),
    "out_edges": fields.List(fields.Integer),
    "status": fields.Integer,
    "extra": fields.Raw,
}

nodes_field = {"nodes": fields.List(fields.Nested(node_field.copy()))}

node_field.update({"log": fields.String(default="")})

node_csv_field = {"data": fields.String}


class Type(fields.Raw):
    def format(self, value):
        return value.__name__


node_params_field = {
    "name": fields.String,
    "description": fields.String,
    "type": Type,
    "required": fields.Boolean,
    "range": fields.List(fields.Integer),
    "enum": fields.List(fields.Raw),
    "default": fields.String,
}

node_description_field = {
    "type": fields.String,
    "name": fields.String,
    "description": fields.String,
    "group": fields.String,
    "icon": fields.String,
    "input_size": fields.Integer,
    "input_type": fields.Integer,
    "output_type": fields.Integer,
    "params": fields.List(fields.Nested(node_params_field)),
}

nodes_description_field = {"data": fields.List(fields.Nested(node_description_field))}

node_predict_data_field = {"type": fields.String, "data": fields.List(fields.Raw)}
node_predict_field = {
    "input": fields.List(fields.Nested(node_predict_data_field)),
    "output": fields.List(fields.Nested(node_predict_data_field)),
    "meta": fields.Nested(meta_field),
}
