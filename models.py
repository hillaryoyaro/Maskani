from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db, login_manager,app
from datetime import datetime, timedelta
from flask_login import UserMixin
#import dateutil.parser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#Creating a class model of Database

class User(db.Model, UserMixin):
    
	id = db.Column(db.Integer, primary_key=True, unique=True)
	first_name = db.Column(db.String(50), nullable=False)
	last_name = db.Column(db.String(50), nullable=False)
	username = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(200), nullable=False)
	role = db.Column(db.String(40), nullable=False)
	image_link = db.Column(db.String(120), nullable=False, default='/static/img/default.jpg')
	phone_number = db.Column(db.String(50), nullable=True)
	location = db.Column(db.String(50), nullable=True)

	fundis = db.relationship('Fundi', backref = "users", lazy=True)
	clients = db.relationship('Client', backref = "users", lazy=True)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	
	@staticmethod
	def verify_reset_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)


	def __repr__(self):
		return f'<User {self.id} {self.first_name} {self.last_name} is a {self.role}>'



class Fundi(db.Model, UserMixin):
	__tablename__ = 'fundis'

	id = db.Column(db.Integer, primary_key=True)
	skills = db.Column(db.String(50), nullable=True)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	jobs = db.relationship("Order", backref = "fundi", lazy=True)
	
# This property returns the User object associated with this Fundi object
	@property
	def user(self):
		return User.query.get(self.user_id)

	def __repr__(self):
# Use the user property to access the first_name and last_name attributes
		return f'<Fundi {self.id} {self.user.first_name} + {self.user.last_name}>'

class Client(db.Model, UserMixin):
	"""
	Client model definition"""
	__tablename__ = 'clients'

	id = db.Column(db.Integer, primary_key=True)
	
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	orders = db.relationship("Order", backref = "client", lazy=True)
	
	@property
	def user(self):
		return User.query.get(self.user_id)

	def __repr__(self):
# Use the user property to access the first_name and last_name attributes
		return f'<Client {self.id} {self.user.first_name} + {self.user.last_name}>'

class Order(db.Model):
	"""Order class definition"""
	__tablename__ = 'orders'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(500), nullable=False)
	location = db.Column(db.String(50), nullable=False)
	price_range = db.Column(db.String(50), nullable=False)
	image_link = db.Column(db.String(50), nullable=True)
	status = db.Column(db.Boolean, nullable=False, default=False)
	service = db.Column(db.String, nullable=False)
	completed = db.Column(db.Boolean, nullable=False, default=False)
	date_created = db.Column(db.DateTime, default=datetime.now(), nullable=False)
	#duration = db.Column(db.String, nullable=False)
	date_due = db.Column(db.DateTime, nullable=False, default=datetime.now() + timedelta(hours=12))
	
	client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
	fundi_id = db.Column(db.Integer, db.ForeignKey("fundis.id"), nullable=True)

	# def set_date_due(self):
	# 	dur = int(self.duration)
	# 	self.date_due = self.date_created + timedelta(hours=dur)
	
	
	@property
	def user(self):
		client = Client.query.get(self.client_id)
		user = User.query.get(client.user_id)
		return user

	def __repr__(self):
		return f'<Order {self.id} {self.title} created by {self.user.first_name} + {self.user.last_name} at {self.date_created}>'
