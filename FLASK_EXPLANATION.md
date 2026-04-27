# Flask Framework - Complete Explanation

## 🎯 What is Flask?

**Flask** is a lightweight Python web framework used to build web applications. It's:
- **Lightweight**: Minimal and flexible
- **Micro-framework**: Only includes essentials
- **Python-based**: Written in Python
- **Easy to learn**: Simple syntax
- **Scalable**: Can build small to large applications

---

## 📊 Flask vs Other Frameworks

| Framework | Size | Complexity | Best For |
|-----------|------|-----------|----------|
| **Flask** | Small | Low | Startups, MVPs, APIs |
| Django | Large | High | Enterprise apps |
| FastAPI | Small | Medium | Modern APIs |
| Bottle | Tiny | Very Low | Micro-services |

---

## 🏗️ How Flask Works

### Basic Concept:

```
User Request (Browser)
    ↓
Flask receives request
    ↓
Routes request to correct function
    ↓
Function processes request
    ↓
Returns response (HTML/JSON)
    ↓
Browser displays response
```

### Simple Example:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
```

**What happens:**
1. Create Flask app
2. Define route `/` 
3. When user visits `/`, `hello()` function runs
4. Returns "Hello, World!"

---

## 🔑 Key Flask Concepts

### 1. **Routes** - URL Mapping

Routes connect URLs to Python functions.

```python
@app.route('/')
def home():
    return "Home Page"

@app.route('/about')
def about():
    return "About Page"

@app.route('/user/<name>')
def user(name):
    return f"Hello, {name}!"
```

**How it works:**
```
User visits: http://localhost:5000/
    ↓
Flask matches route: @app.route('/')
    ↓
Calls: home() function
    ↓
Returns: "Home Page"
```

### 2. **HTTP Methods** - Request Types

```python
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Handle form submission
        data = request.form.get('name')
        return f"Received: {data}"
    else:
        # Show form
        return "Show form"
```

**Common methods:**
- **GET**: Retrieve data (no side effects)
- **POST**: Submit data (creates/updates)
- **PUT**: Update data
- **DELETE**: Remove data

### 3. **Request Object** - Access User Data

```python
from flask import request

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    city = request.form.get('city')
    bhk = request.form.get('bhk')
    
    # Get URL parameters
    page = request.args.get('page')
    
    # Get JSON data
    data = request.get_json()
    
    return f"City: {city}, BHK: {bhk}"
```

**In your project:**
```python
city = request.form.get('city')           # From form
bhk = max(1, int(request.form.get('bhk', 1)))  # With default
```

### 4. **Response Object** - Send Data Back

```python
from flask import render_template, jsonify

# Return HTML
@app.route('/')
def home():
    return render_template('index.html')

# Return JSON
@app.route('/api/data')
def api():
    return jsonify({'status': 'success', 'data': [1, 2, 3]})

# Return plain text
@app.route('/text')
def text():
    return "Plain text response"
```

### 5. **Templates** - Dynamic HTML

Flask uses **Jinja2** templating engine.

```python
from flask import render_template

@app.route('/')
def home():
    cities = ['Delhi', 'Mumbai', 'Bangalore']
    return render_template('index.html', cities=cities)
```

**In template (index.html):**
```html
<select>
    {% for city in cities %}
    <option>{{ city }}</option>
    {% endfor %}
</select>
```

**Jinja2 features:**
- `{{ variable }}` - Display variable
- `{% for item in list %}` - Loop
- `{% if condition %}` - Conditional
- `{% extends "base.html" %}` - Inheritance

### 6. **Static Files** - CSS, JS, Images

```python
app = Flask(__name__, static_folder='static')
```

**In template:**
```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<script src="{{ url_for('static', filename='script.js') }}"></script>
```

**Folder structure:**
```
project/
├── static/
│   ├── style.css
│   ├── script.js
│   └── images/
└── templates/
    └── index.html
```

---

## 🎯 Your Project's Flask Usage

### 1. **App Factory Pattern**

```python
# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app
```

**Why?**
✅ Cleaner code organization
✅ Easy testing
✅ Multiple app instances
✅ Better scalability

### 2. **Blueprints** - Modular Routes

```python
# app/routes.py
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html', cities=cities)

@main.route('/predict', methods=['POST'])
def predict():
    # Main logic here
    return render_template('results.html', ...)
```

**Why Blueprints?**
✅ Organize routes into modules
✅ Reusable route groups
✅ Easier to maintain
✅ Better for large projects

### 3. **Request Handling**

```python
@main.route('/predict', methods=['POST'])
def predict():
    # Get form data
    city = request.form.get('city')
    bhk = int(request.form.get('bhk'))
    area = float(request.form.get('area'))
    budget = float(request.form.get('budget')) * 100000
    
    # Process data
    user_input = {
        'City': city,
        'BHK': bhk,
        'CarpetArea_sqft': area
    }
    
    # Call functions
    price_data = predict_price(user_input)
    recommendations = recommend_properties(user_input, budget)
    
    # Return response
    return render_template('results.html',
                         price=price_data,
                         results=recommendations)
```

### 4. **Template Rendering**

```python
# In routes.py
return render_template('results.html',
                      price=price_data,
                      results=recommendations,
                      city=city,
                      affordability_label=affordability_label)
```

**In results.html:**
```html
<h2>₹ {{ price.predicted_price }}</h2>
<p>Range: ₹ {{ price.lower }} - ₹ {{ price.upper }}</p>

{% for property in results %}
<div class="card">
    <h3>{{ property.BHK }} BHK</h3>
    <p>Price: ₹ {{ property.Price_INR }}</p>
    <p>Match: {{ property.MatchPercent }}%</p>
</div>
{% endfor %}
```

### 5. **Error Handling**

```python
@main.route('/predict', methods=['POST'])
def predict():
    try:
        # All processing
        city = request.form.get('city')
        bhk = int(request.form.get('bhk'))
        # ... more code
        
        return render_template('results.html', ...)
    
    except ValueError:
        return render_template('index.html', 
                             error="Invalid input")
    except Exception as e:
        return render_template('index.html',
                             error=f"Error: {str(e)}")
```

---

## 🔄 Flask Request-Response Cycle

### Step-by-Step:

```
1. USER ACTION
   User fills form and clicks "Find Properties"
   
2. HTTP REQUEST
   Browser sends POST request to /predict
   Request includes form data:
   - city: "Delhi"
   - bhk: "2"
   - area: "1200"
   - budget: "50"
   
3. FLASK RECEIVES REQUEST
   Flask receives POST /predict request
   
4. ROUTE MATCHING
   Flask matches URL to route:
   @main.route('/predict', methods=['POST'])
   
5. FUNCTION EXECUTION
   predict() function runs
   - Extracts form data using request.form.get()
   - Validates inputs
   - Calls predict_price()
   - Calls recommend_properties()
   - Processes results
   
6. TEMPLATE RENDERING
   render_template('results.html', data=...)
   - Loads results.html template
   - Replaces {{ variables }} with actual data
   - Generates HTML
   
7. HTTP RESPONSE
   Flask sends HTML response to browser
   
8. BROWSER DISPLAYS
   Browser renders HTML
   User sees results page
```

---

## 📝 Flask Decorators Explained

### @app.route() - URL Routing

```python
@app.route('/')                    # Home page
@app.route('/about')               # About page
@app.route('/user/<name>')         # Dynamic URL
@app.route('/post/<int:id>')       # URL with type
@app.route('/search', methods=['GET', 'POST'])  # Multiple methods
```

### @app.before_request - Before Each Request

```python
@app.before_request
def before_request():
    print("Request received")
    # Can check authentication, etc.
```

### @app.after_request - After Each Request

```python
@app.after_request
def after_request(response):
    print("Response sent")
    return response
```

### @app.errorhandler - Handle Errors

```python
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500
```

---

## 🛠️ Flask Configuration

### Development vs Production

```python
# Development
app.run(debug=True)           # Auto-reload on changes
app.run(debug=True, port=5000)  # Custom port

# Production
app.run(debug=False)          # No auto-reload
app.config['ENV'] = 'production'
```

### Configuration Variables

```python
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
```

---

## 📦 Flask Extensions Used in Your Project

### 1. **Jinja2** - Templating
```python
from flask import render_template
render_template('index.html', cities=cities)
```

### 2. **Werkzeug** - WSGI Utilities
```python
from werkzeug.utils import secure_filename
```

### 3. **Click** - CLI
```python
@app.cli.command()
def init_db():
    # Initialize database
    pass
```

---

## 🔐 Flask Security Features

### 1. **CSRF Protection**
```python
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

### 2. **Session Management**
```python
from flask import session
session['user_id'] = 123
user_id = session.get('user_id')
```

### 3. **Input Validation**
```python
# Always validate user input
city = request.form.get('city')
if not city:
    return "City is required", 400
```

---

## 📊 Your Project's Flask Architecture

```
main.py
    ↓
app/__init__.py (create_app)
    ├─ Creates Flask instance
    ├─ Sets template folder
    ├─ Sets static folder
    └─ Registers blueprints
        ↓
    app/routes.py (Blueprint)
        ├─ @main.route('/') → home()
        └─ @main.route('/predict', methods=['POST']) → predict()
            ├─ request.form.get() → Get user input
            ├─ predict_price() → ML prediction
            ├─ recommend_properties() → Recommendations
            └─ render_template() → Return HTML
                ↓
            templates/
                ├─ base.html (base template)
                ├─ index.html (home page)
                └─ results.html (results page)
                    ↓
            static/
                └─ style.css (styling)
```

---

## 💡 Why Flask for Your Project?

✅ **Lightweight**: Perfect for ML applications
✅ **Flexible**: Easy to integrate ML models
✅ **Fast**: Quick development
✅ **Scalable**: Can grow with project
✅ **Popular**: Large community support
✅ **Easy to learn**: Simple syntax
✅ **Perfect for APIs**: Easy to build REST APIs

---

## 🚀 Flask Development Workflow

### 1. **Create App**
```python
app = Flask(__name__)
```

### 2. **Define Routes**
```python
@app.route('/')
def home():
    return "Hello"
```

### 3. **Run Server**
```python
app.run(debug=True)
```

### 4. **Test in Browser**
```
http://localhost:5000
```

### 5. **Make Changes**
- Edit code
- Flask auto-reloads (debug=True)
- Refresh browser

---

## 📈 Flask Request Flow in Your Project

```
Browser Request
    ↓
http://localhost:5000/predict (POST)
    ↓
Flask receives request
    ↓
Routes to: @main.route('/predict', methods=['POST'])
    ↓
predict() function executes:
    1. request.form.get('city') → Get city
    2. request.form.get('bhk') → Get BHK
    3. request.form.get('area') → Get area
    4. request.form.get('budget') → Get budget
    ↓
Process data:
    1. Validate inputs
    2. Get coordinates
    3. Calculate accessibility
    4. Create user_input dict
    ↓
Call functions:
    1. predict_price(user_input) → Price prediction
    2. recommend_properties(user_input, budget) → Recommendations
    ↓
Prepare response:
    1. Calculate affordability
    2. Sort results
    3. Prepare template data
    ↓
render_template('results.html', price=..., results=...)
    ↓
Jinja2 renders template:
    1. Replaces {{ price.predicted_price }}
    2. Loops through {% for p in results %}
    3. Generates HTML
    ↓
Flask sends HTML response
    ↓
Browser receives HTML
    ↓
Browser displays results page
```

---

## 🎓 For Your Capstone Presentation

**You can explain:**

> "I used **Flask**, a lightweight Python web framework, to build the backend of my SmartHome Finder application. Flask provides:
>
> 1. **Routing**: Maps URLs to Python functions using decorators (@app.route)
> 2. **Request Handling**: Easily access form data using request.form.get()
> 3. **Template Rendering**: Uses Jinja2 to dynamically generate HTML with data
> 4. **Blueprints**: Organizes routes into modular components
> 5. **Error Handling**: Try-except blocks for robust error management
>
> The request flow is:
> - User submits form → Flask receives POST request
> - Routes to /predict endpoint → predict() function executes
> - Extracts form data → Validates inputs
> - Calls ML prediction and recommendation functions
> - Renders results.html template with data
> - Returns HTML response to browser
>
> Flask's simplicity and flexibility made it perfect for integrating machine learning models with a web interface."

---

**Flask is the backbone of your web application! 🎓**
