from marshmallow import fields, Schema
class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
class UserProfileSchema(Schema):
    id = fields.String()
    email = fields.String()
    avatar = fields.String()
    fullname = fields.String()
    bio = fields.String()
    date_of_birth = fields.DateTime()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
class UserSchema(Schema):
     id = fields.String()
     username = fields.String()
     points = fields.Integer()
     is_active = fields.Boolean()
     created_at = fields.DateTime()
     updated_at = fields.DateTime()
     profile = fields.Nested(UserProfileSchema, dump_only=True)
     roles = fields.Nested(RoleSchema, many=True, dump_only=True)


   