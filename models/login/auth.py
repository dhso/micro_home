# -*- coding: utf-8 -*-

from flask_user import SQLAlchemyAdapter, UserManager, UserMixin
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class UserModel:
    def __init__(self, db, app):
        self.db = db
        self.app = app
        # Define the User data model. Make sure to add flask.ext.user UserMixin!!

    def user_model(self):
    	class User(self.db.Model, UserMixin):
            id = self.db.Column(self.db.Integer, primary_key=True)
    
            # User authentication information
            username = self.db.Column(self.db.String(50), nullable=False, unique=True)
            password = self.db.Column(self.db.String(255), nullable=False, server_default='')
            reset_password_token = self.db.Column(self.db.String(100), nullable=False, server_default='')
    
            # User email information
            email = self.db.Column(self.db.String(255), nullable=False, unique=True)
            confirmed_at = self.db.Column(self.db.DateTime())
        
            # User information
            active = self.db.Column('is_active', self.db.Boolean(), nullable=False, server_default='0')
            first_name = self.db.Column(self.db.String(100), nullable=False, server_default='')
            last_name = self.db.Column(self.db.String(100), nullable=False, server_default='')
    
            # Relationships
            roles = self.db.relationship('Role', secondary='user_roles',
                    backref=self.db.backref('users', lazy='dynamic'))
    
        # Define the Role data model
        class Role(self.db.Model):
            id = self.db.Column(self.db.Integer(), primary_key=True)
            name = self.db.Column(self.db.String(50), unique=True)
    
        # Define the UserRoles data model
        class UserRoles(self.db.Model):
            id = self.db.Column(self.db.Integer(), primary_key=True)
            user_id = self.db.Column(self.db.Integer(), self.db.ForeignKey('user.id', ondelete='CASCADE'))
            role_id = self.db.Column(self.db.Integer(), self.db.ForeignKey('role.id', ondelete='CASCADE'))

        # Reset all the database tables
        self.db.create_all()

        # Setup Flask-User
        db_adapter = SQLAlchemyAdapter(self.db,  User)
        user_manager = UserManager(db_adapter, self.app)

        # Create 'user007' user with 'secret' and 'agent' roles
        if not User.query.filter(User.username=='admin').first():
            user_admin = User(username='admin', email='admin@example.com', active=True, password=user_manager.hash_password('admin'))
            user_admin.roles.append(Role(name='admin'))
            user_admin.roles.append(Role(name='secret'))
            self.db.session.add(user_admin)
            self.db.session.commit()