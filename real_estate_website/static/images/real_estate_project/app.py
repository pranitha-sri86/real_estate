from flask import Flask, render_template, url_for

app = Flask(__name__)

properties = [
    {
        "id": 1,
        "title": "Luxury Villa in Beverly Hills",
        "location": "Beverly Hills, CA",
        "price": "2,500,000",
        "bedrooms": 5,
        "size": 4500,
        "image": "villa1.jpg"
    },
    {
        "id": 2,
        "title": "Modern Apartment in New York",
        "location": "Manhattan, NY",
        "price": "1,200,000",
        "bedrooms": 3,
        "size": 1800,
        "image": "apartment1.jpg"
    },
    {
        "id": 3,
        "title": "Beachside House in Miami",
        "location": "Miami, FL",
        "price": "3,800,000",
        "bedrooms": 6,
        "size": 5200,
        "image": "beachhouse1.jpg"
    }
]

agents = [
    {"name": "John Carter", "role": "Senior Agent", "image": "agent1.jpg"},
    {"name": "Sophia Lee", "role": "Luxury Specialist", "image": "agent2.jpg"},
    {"name": "Michael Smith", "role": "Commercial Expert", "image": "agent3.jpg"}
]

@app.route("/")
def home():
    return render_template("index.html", properties=properties, agents=agents)

@app.route("/properties")
def show_properties():
    return render_template("properties.html", properties=properties)

@app.route("/property/<int:id>")
def property_details(id):
    property_item = next((p for p in properties if p["id"] == id), None)
    return render_template("property_details.html", property=property_item)

@app.route("/amenities")
def amenities():
    return render_template("amenities.html")

@app.route("/agents")
def agents_page():
    return render_template("agents.html", agents=agents)

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
