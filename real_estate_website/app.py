# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

# --- Configuration ---
app = Flask(__name__)
app.secret_key = 'supersecretkey_realestate_secure_this_in_production' # MUST be a strong secret key
# Configure SQLite database (database file will be created in the project root)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///realestate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Model ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Hashes the password using Werkzeug for secure storage."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks the hashed password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# --- Helper Function ---
def generate_id():
    return str(uuid.uuid4())[:8]

# --- Global Data and Image URLs ---

HEADER_BG_URL = 'https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'
COMPANY_IMAGE_URL = 'https://images.pexels.com/photos/3184405/pexels-photo-3184405.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'

PROPERTIES = [
    {
        'id': generate_id(),
        'title': 'Luxury Downtown Apartment',
        'location': 'New York, USA',
        'price': '$1,200,000',
        'image_url': 'https://images.pexels.com/photos/1643383/pexels-photo-1643383.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'beds': 3,
        'area_sqft': 1500,
        'type': 'Apartment',
        'additional_info': 'High-rise with stunning city views, modern finishes, and concierge service.',
        'keywords': 'New York, downtown, apartment, 3-bed, luxury, 1.2M'
    },
    {
        'id': generate_id(),
        'title': 'Spacious Suburban Villa',
        'location': 'Los Angeles, USA',
        'price': '$2,500,000',
        'image_url': 'https://images.pexels.com/photos/186077/pexels-photo-186077.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'beds': 5,
        'area_sqft': 4000,
        'type': 'Villa',
        'additional_info': 'Large backyard, private pool, excellent school district. Ideal for families.',
        'keywords': 'Los Angeles, suburban, villa, 5-bed, family, 2.5M'
    },
    {
        'id': generate_id(),
        'title': 'Cozy Mountain Cabin',
        'location': 'Denver, USA',
        'price': '$450,000',
        'image_url': 'https://images.pexels.com/photos/208736/pexels-photo-208736.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'beds': 2,
        'area_sqft': 800,
        'type': 'Cabin',
        'additional_info': 'Perfect getaway spot. Close to ski slopes and hiking trails. Fully furnished.',
        'keywords': 'Denver, mountain, cabin, 2-bed, vacation, 450K'
    },
    {
        'id': generate_id(),
        'title': 'Modern Loft',
        'location': 'San Francisco, USA',
        'price': '$950,000',
        'image_url': 'https://images.pexels.com/photos/271743/pexels-photo-271743.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'beds': 1,
        'area_sqft': 900,
        'type': 'Apartment',
        'additional_info': 'Open-concept, industrial design, prime city location.',
        'keywords': 'San Francisco, loft, apartment, 1-bed, modern, 950K'
    },
    {
        'id': generate_id(),
        'title': 'Beachfront House',
        'location': 'Miami, USA',
        'price': '$3,800,000',
        'image_url': 'https://images.pexels.com/photos/2089698/pexels-photo-2089698.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'beds': 4,
        'area_sqft': 3200,
        'type': 'House',
        'additional_info': 'Direct beach access, stunning ocean views, large terrace.',
        'keywords': 'Miami, beach, house, 4-bed, luxury, 3.8M'
    },
    {
        'id': generate_id(),
        'title': 'Rural Farmhouse',
        'location': 'Austin, USA',
        'price': '$750,000',
        'image_url': 'https://images.pexels.com/photos/259647/pexels-photo-259647.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'beds': 4,
        'area_sqft': 2500,
        'type': 'House',
        'additional_info': 'Spacious land, quiet environment, perfect for farming.',
        'keywords': 'Austin, rural, farmhouse, 4-bed, quiet, 750K'
    },
    {
        'id': generate_id(),
        'title': 'Chic Studio',
        'location': 'Seattle, USA',
        'price': '$300,000',
        'image_url': 'https://images.pexels.com/photos/1396122/pexels-photo-1396122.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'beds': 0,
        'area_sqft': 500,
        'type': 'Studio',
        'additional_info': 'Efficient layout, close to public transport, ideal for singles.',
        'keywords': 'Seattle, studio, apartment, 0-bed, cheap, 300K'
    },
    {
        'id': generate_id(),
        'title': 'Penthouse Suite',
        'location': 'Chicago, USA',
        'price': '$5,000,000',
        'image_url': 'https://images.pexels.com/photos/1571471/pexels-photo-1571471.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'beds': 4,
        'area_sqft': 5000,
        'type': 'Apartment',
        'additional_info': 'Top floor, exclusive elevator access, panoramic city views.',
        'keywords': 'Chicago, penthouse, apartment, 4-bed, exclusive, 5M'
    },
    {
        'id': generate_id(),
        'title': 'Townhouse with Garden',
        'location': 'Boston, USA',
        'price': '$1,100,000',
        'image_url': 'https://images.pexels.com/photos/1475938/pexels-photo-1475938.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        'beds': 3,
        'area_sqft': 1800,
        'type': 'Townhouse',
        'additional_info': 'Three stories, small private garden, historic neighborhood.',
        'keywords': 'Boston, townhouse, 3-bed, historic, 1.1M'
    }
]

AGENTS = [
    {'name': 'Jane Doe', 'designation': 'Senior Broker', 'phone': '(555) 123-4567', 'email': 'jane.doe@estate.com', 'photo_url': 'https://randomuser.me/api/portraits/women/44.jpg'},
    {'name': 'John Smith', 'designation': 'Sales Associate', 'phone': '(555) 987-6543', 'email': 'john.smith@estate.com', 'photo_url': 'https://randomuser.me/api/portraits/men/55.jpg'},
    {'name': 'Alex Lee', 'designation': 'Investment Specialist', 'phone': '(555) 555-1212', 'email': 'alex.lee@estate.com', 'photo_url': 'https://randomuser.me/api/portraits/lego/3.jpg'},
]

REVIEWS = [
    {'name': 'Sarah K.', 'photo_url': 'https://randomuser.me/api/portraits/women/12.jpg', 'feedback': 'The agents were incredibly professional and helped us find our dream home in a tough market. Highly recommend!', 'rating': 5},
    {'name': 'Mark L.', 'photo_url': 'https://randomuser.me/api/portraits/men/21.jpg', 'feedback': 'Seamless transaction from start to finish. The details provided were accurate, and the team was always available for questions.', 'rating': 5},
    {'name': 'David O.', 'photo_url': 'https://randomuser.me/api/portraits/women/3.jpg', 'feedback': 'Found a great property below budget. Their search feature is very effective!', 'rating': 4},
]

# --- Flask Context Processor ---

# Makes variables available in ALL templates
@app.context_processor
def inject_global_vars():
    # Check if user is logged in
    logged_in = 'user_id' in session
    username = session.get('username') if logged_in else None
    return dict(
        header_bg_url=HEADER_BG_URL,
        logged_in=logged_in,
        current_username=username,
        company_image_url=COMPANY_IMAGE_URL # Also pass the company image URL
    )

# --- General Routes ---

@app.route('/')
def index():
    """Renders the main page with all sections."""
    return render_template(
        'index.html',
        properties=PROPERTIES,
        agents=AGENTS,
        reviews=REVIEWS,
    )

@app.route('/property/<property_id>')
def property_details(property_id):
    """Renders the detailed page for a specific property."""
    property_data = next((p for p in PROPERTIES if p['id'] == property_id), None)
    if property_data:
        return render_template('property_details.html', property=property_data)
    flash('Property not found.', 'danger')
    return redirect(url_for('index'))

@app.route('/search')
def search():
    """Handles property search functionality."""
    query = request.args.get('q', '').lower()
    
    if not query:
        flash('Please enter a search term.', 'warning')
        return redirect(url_for('index'))

    # Simple keyword search logic across location, type, and price keywords
    search_results = [
        p for p in PROPERTIES
        if query in p['keywords'].lower() or query in p['location'].lower() or query in p['type'].lower()
    ]
    
    return render_template('search_results.html', query=query, properties=search_results)

@app.route('/contact', methods=['POST'])
def handle_contact_form():
    """Handles the contact form submission."""
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')

    if name and email and message:
        # Placeholder for database storage/email sending logic
        print(f"New Contact Form Submission: Name={name}, Email={email}, Phone={phone}, Message={message}")
        flash('Thank you for your message! We will get back to you shortly.', 'success')
    else:
        flash('Error: Please fill in all required fields.', 'danger')

    return redirect(url_for('index') + '#contact')

# --- Authentication Routes ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles new user registration."""
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Simple validation
        if not (username and email and password):
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('register'))

        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Login successful: Set session variables
            session['user_id'] = user.id
            session['username'] = user.username
            
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Handles user logout."""
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# --- Main Execution ---

if __name__ == '__main__':
    with app.app_context():
        # Creates the database file and tables if they don't exist (Fix for Flask 2.3+ AttributeError)
        db.create_all() 
    app.run(debug=True)