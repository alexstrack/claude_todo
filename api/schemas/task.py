from marshmallow import Schema, fields, validate, pre_dump, post_load
from datetime import datetime


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True, validate=validate.Length(min=1))
    due_date = fields.Str(required=True)  # Keep as string to match SQLite storage
    status = fields.Bool(dump_default=False)
    created_at = fields.Str(dump_only=True)  # Keep as string to match SQLite storage
    
    @pre_dump
    def prepare_data(self, data, **kwargs):
        # Convert sqlite3.Row to dict
        if hasattr(data, 'keys'):
            data = dict(data)
        
        # Ensure we have a proper dict
        data_dict = {}
        for key in ['id', 'description', 'due_date', 'status', 'created_at']:
            if key in data:
                data_dict[key] = data[key]
        
        # Convert status to boolean
        if 'status' in data_dict:
            data_dict['status'] = bool(data_dict['status'])
            
        return data_dict
        
    @post_load
    def format_dates(self, data, **kwargs):
        # Ensure dates are in the format SQLite expects
        if 'due_date' in data and data['due_date']:
            # Ensure the date is in YYYY-MM-DD format
            if isinstance(data['due_date'], datetime):
                data['due_date'] = data['due_date'].strftime('%Y-%m-%d')
        return data


class TaskUpdateSchema(Schema):
    description = fields.Str(validate=validate.Length(min=1))
    due_date = fields.Str()  # Keep as string to match SQLite storage
    status = fields.Bool()