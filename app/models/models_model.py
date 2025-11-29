
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

# (Many-to-Many): Giữa User và Role.
user_roles_table = db.Table('user_roles',
    db.Column('user_id', db.String(36), db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)
event_participants_table = db.Table('event_participants',
    db.Column('user_id', db.String(36), db.ForeignKey('users.id'), primary_key=True),
    db.Column('organized_event_id', db.Integer, db.ForeignKey('organized_events.id'), primary_key=True)
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

    # (One-to-one): Giữa User và UserProfile.
    profile = db.relationship('UserProfile', back_populates='user', uselist=False, cascade="all, delete-orphan")
    # (One-to-one): Giữa User và Organization.
    organization = db.relationship('Organization', back_populates='owner', uselist=False, cascade="all, delete-orphan")

    # (Many-to-Many): Giữa User và Role.
    roles = db.relationship('Role', secondary=user_roles_table, backref=db.backref('users', lazy='dynamic'))

    # (One-to-many): giữa User và Challenge.
    challenges = db.relationship('Challenge', back_populates='user', lazy='dynamic')

    uploads = db.relationship(
        'Media',
        backref='uploader',          # Bên Media sẽ có biến .uploader
        cascade="all, delete-orphan", # Xóa User -> Xóa sạch ảnh do nó upload
        lazy='dynamic',
        foreign_keys='Media.uploaded_by_user_id' # Chỉ định rõ khóa ngoại
    )


   
    
       
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password): 
        return check_password_hash(self.password, password)
class UserProfile(db.Model):
        __tablename__ = 'user_profile'
        id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
        email = db.Column(db.String(255), nullable=True)
        fullname = db.Column(db.String(255), nullable=True)
        bio = db.Column(db.String(255), nullable=True)
        date_of_birth = db.Column(db.DateTime(), nullable=True)
        created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
        updated_at = db.Column(db.DateTime(), nullable=False, default=db.func.now(), onupdate=db.func.now())

        # (One-to-one): Giữa User và UserProfile.
        user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, unique=True)
        user = db.relationship('User', back_populates='profile')

        # (One-to-one): giữa UserProfile và media
        avatar_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
        avatar = db.relationship(
            'Media',
            back_populates='profile_avatar',
            uselist=False, cascade="all, delete-orphan",
            lazy='joined',
            single_parent=True)




    
class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

class Organization(db.Model):
    __tablename__ = 'organization'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    tax_code = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False, default='pending') # approved , rejected
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    # (One-to-one): Giữa User và Organization.
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, unique=True)
    owner = db.relationship('User', back_populates='organization')

    #(1) (One-to-Many): Giữa Organization và Challenge.
    challenges= db.relationship('Challenge', back_populates='organization', lazy='dynamic')

    # (One-to-one): giữa UserProfile và media
    logo_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
    logo_url = db.relationship('Media', back_populates='organization_logo')

    # (One-to-Many): Giữa Organization và OrganizedEvent.
    organized_events = db.relationship('Organized_Events', back_populates='organization', lazy='dynamic')






class Challenge (db.Model):
    __tablename__ = 'challenges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    is_featured = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String(255), nullable=False, default='pending') #('idea', 'pending_approval', 'approved', 'in_progress', 'completed')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    # (One-to-Many): giữa Challenge và Media.
    images = db.relationship('Media', back_populates='challenge', lazy='dynamic')

    # N (One-to-Many): Giữa Organization và Challenge.
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=True)
    organization = db.relationship('Organization', back_populates='challenges')

    # N (One-to-Many): Giữa User và Challenge.
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', back_populates='challenges')

    # (One-to-Many): Giữa Challenge và Organized_Events.
    organized_events = db.relationship('Organized_Events', back_populates='challenge', lazy='dynamic')
    # (one to many): giữa challenge và categories_challenges
    category = db.relationship('Category', back_populates='challenges')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(255), nullable=False, unique=True)
    secure_url = db.Column(db.String(255), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False, default='image')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    
    uploaded_by_user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)

    # (One-to-one): Giữa User và Media.
    profile_avatar = db.relationship('UserProfile', back_populates='avatar', foreign_keys='UserProfile.avatar_id' )

    # (One-to-one): Giữa User và Media.
    organization_logo = db.relationship('Organization', back_populates='logo_url', foreign_keys=[Organization.logo_id])

    # (One-to-Many): Giữa Challenge và Media.
    challenge = db.relationship('Challenge', back_populates='images')
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=True)

    # (one-to-one): giữa media và categories_challenges
    category = db.relationship('Category', back_populates='image', foreign_keys='Category.image_id')



class Organized_Events(db.Model): 
    __tablename__ = 'organized_events'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, default=db.func.now())
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(255), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    # (one-to-many) giữa organized_events và challenge
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=True)
    challenge = db.relationship('Challenge', back_populates='organized_events')

    # (one-to-many) giữa organized_events và organization
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=True)
    organization = db.relationship('Organization', back_populates='organized_events')

    # (Many-to-Many): Giữa User và Organized_Events.
    participants = db.relationship('User', secondary=event_participants_table, backref=db.backref('organized_events', lazy='dynamic'))

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    # (one-to_many) giữ categories_challenges và ảnh
    image = db.relationship('Media', back_populates='category')
    image_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)

    # (one-to_many) giữa categories_challenges và challenge
    challenges = db.relationship('Challenge', back_populates='category',lazy='dynamic')






   

    





    

 

    



    
















    
    
    

   
    

    
    