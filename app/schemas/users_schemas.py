from marshmallow import fields, Schema
class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
class UserSchema(Schema):
     id = fields.String()
     username = fields.String()
     email = fields.String()
     avatar = fields.String()
     is_active = fields.Boolean()
     created_at = fields.DateTime()
     updated_at = fields.DateTime()
     roles = fields.Nested(RoleSchema, many=True, dump_only=True)
   