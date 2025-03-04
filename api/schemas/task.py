from marshmallow import Schema, fields, validate, pre_dump
from datetime import datetime


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True, validate=validate.Length(min=1))
    due_date = fields.Str(required=True)  # Keep as string to match SQLite storage
    status = fields.Bool(dump_default=False)
    created_at = fields.Str(dump_only=True)  # Keep as string to match SQLite storage
    
    @pre_dump
    def prepare_data(self, data, **kwargs):
        # If data is a dict-like object (like sqlite3.Row), convert to dict
        if hasattr(data, 'keys'):
            data = dict(data)
            
        # Format the status to ensure it's a boolean
        if 'status' in data and not isinstance(data['status'], bool):
            data['status'] = bool(data['status'])
            
        return data


class TaskUpdateSchema(Schema):
    description = fields.Str(validate=validate.Length(min=1))
    due_date = fields.Str()  # Keep as string to match SQLite storage
    status = fields.Bool()