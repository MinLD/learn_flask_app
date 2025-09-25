# app/models/auth_model.py
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token,  get_jwt
from uuid import uuid4

user_roles_table = db.Table('user_roles',
    db.Column('user_id', db.String(36), db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Role {self.name}>'
    @classmethod
    def get_role_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    def save(self):
        db.session.add(self)
        db.session.commit()




    

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean(), nullable=False, default=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, default=db.func.now(), onupdate=db.func.now())
    roles = db.relationship('Role', secondary=user_roles_table, backref=db.backref('users', lazy='dynamic'))
    def __repr__(self):
        return '<User {self.username}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    
    def check_password(self, password): 
        return check_password_hash(self.password, password)
    
    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first() 

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


    #Server
    @classmethod
    def model_register(cls,data ):
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = Role.get_role_by_name('user')

        
        if not username or not password or not email:
            return None, "Thiếu thông tin bắt buộc hoặc thông tin rỗng (username, password, email)"
        if cls.get_user_by_username(username):
            return None, "Tên đăng nhập đã tồn tại"
        if cls.get_user_by_email(email):
            return None, "Email đã tồn tại"
        
        
        new_user = cls(username=username, email=email, roles=[role])
        new_user.set_password(password)
        
        new_user.save()
        
        return new_user, None
    
    @classmethod
    def generate_tokens(cls, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return None, None, "Thiếu username hoặc password"

        user = cls.get_user_by_username(username=data.get('username'))
        if user and user.check_password(password=data.get('password')):
            user_roles = [role.name for role in user.roles]
            additional_claims = {"roles": user_roles}
            access_token = create_access_token(
            identity=str(user.id), 
            additional_claims=additional_claims
        )
            refresh_token = create_refresh_token(identity=user.id)
            return access_token, refresh_token, None
        
        return None, None, "Username hoặc password không chính xác"
    

    def whoami():
        claims = get_jwt()
        return "hello", claims
    
    
    

   
    

    
    