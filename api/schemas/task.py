from marshmallow import Schema, fields, validate


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True, validate=validate.Length(min=1))
    due_date = fields.Date(required=True)
    status = fields.Bool(dump_default=False)
    created_at = fields.DateTime(dump_only=True)


class TaskUpdateSchema(Schema):
    description = fields.Str(validate=validate.Length(min=1))
    due_date = fields.Date()
    status = fields.Bool()