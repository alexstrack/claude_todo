from marshmallow import Schema, fields


class TaskSchema(Schema):
    """Schema for task serialization and validation."""
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True)
    due_date = fields.Str(required=True)  # Using string format for dates
    status = fields.Bool(dump_default=False)
    created_at = fields.Str(dump_only=True)


class TaskUpdateSchema(Schema):
    """Schema for task updates."""
    description = fields.Str()
    due_date = fields.Str()
    status = fields.Bool()