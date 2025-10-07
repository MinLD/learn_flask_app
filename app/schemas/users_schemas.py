from marshmallow import fields, Schema
class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
class MediaSchema(Schema):
    id = fields.Integer()
    public_id = fields.String()
    secure_url = fields.String()
    resource_type = fields.String()
    created_at = fields.DateTime()
class UserProfileSchema(Schema):
    id = fields.String()
    email = fields.String()
    avatar = fields.Nested(MediaSchema, dump_only=True)
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

class OrganizationSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    logo_url = fields.Nested(MediaSchema, dump_only=True)
    tax_code = fields.String()
    website = fields.String()
    email = fields.String()
    phone = fields.String()
    address = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    # owner = fields.Nested(UserSchema, dump_only=True)

class  ChallengeSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    location = fields.String()
    is_featured = fields.Boolean()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    organization = fields.Nested(OrganizationSchema, dump_only=True)
    user = fields.Nested(UserSchema, dump_only=True)
    images = fields.Nested(MediaSchema, many=True, dump_only=True)

class UserIDSchema(Schema):
     id = fields.String()

class Organized_EventsSchema(Schema):
    id = fields.Integer()
    challenge = fields.Nested(ChallengeSchema, dump_only=True)
    organization = fields.Nested(OrganizationSchema, dump_only=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    status = fields.String()
    participants = fields.Nested(UserIDSchema, dump_only=True, many=True)




   