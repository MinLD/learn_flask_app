
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

# (Many-to-Many): Giữa User và Role.
user_roles_table = db.Table('user_roles',
    db.Column('user_id', db.String(36), db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)




class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean(), nullable=False, default=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, default=db.func.now(), onupdate=db.func.now())

    profile = db.relationship('UserProfile', back_populates='user', uselist=False, cascade="all, delete-orphan")
    organization = db.relationship('Organization', back_populates='owner', uselist=False, cascade="all, delete-orphan")
    roles = db.relationship('Role', secondary=user_roles_table, backref=db.backref('users', lazy='dynamic'))

   
    
       
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password): 
        return check_password_hash(self.password, password)
class UserProfile(db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    email = db.Column(db.String(255), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    fullname = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.String(255), nullable=True)
    date_of_birth = db.Column(db.DateTime(), nullable=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, default=db.func.now(), onupdate=db.func.now())

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, unique=True)
    user = db.relationship('User', back_populates='profile')
    
class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

class Organization(db.Model):
    __tablename__ = 'organization'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())
    description = db.Column(db.String(255), nullable=False)
    logo_url = db.Column(db.String(255), nullable=False)
    tax_code = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False, default='pending')

    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, unique=True)
    owner = db.relationship('User', back_populates='organization')









    
    
    

   
    

    
    