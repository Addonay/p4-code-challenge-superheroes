from flask import Flask, make_response, jsonify, request, redirect, url_for
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return redirect(url_for('create_hero_power'))


# Route to add a new hero
@app.route('/add_hero', methods=['POST'])
def add_hero():
    data = request.get_json()
    if 'name' not in data or 'supername' not in data:
        return jsonify({'error': 'Missing name or supername'}), 400
    new_hero = Hero(name=data['name'], supername=data['supername'])
    db.session.add(new_hero)
    db.session.commit()
    return jsonify({'message': 'Hero added successfully'}), 201


# Route to add a new power
@app.route('/add_power', methods=['POST'])
def add_power():
    data = request.get_json()
    if 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Missing name or description'}), 400
    new_power = Power(name=data['name'], description=data['description'])
    db.session.add(new_power)
    db.session.commit()
    return jsonify({'message': 'Power added successfully'}), 201


# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.supername} for hero in heroes]  # Use 'supername' instead of 'super_name'
    return jsonify(hero_data)

# GET /heroes/:id
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({'error': 'Hero not found'}), 404
    
    powers = [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
    hero_data = {'id': hero.id, 'name': hero.name, 'supername': hero.supername, 'powers': powers}  # Use 'supername' instead of 'super_name'
    return jsonify(hero_data)

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_data)

# GET /powers/:id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404
    power_data = {'id': power.id, 'name': power.name, 'description': power.description}
    return jsonify(power_data)

# PATCH /powers/:id
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404
    
    data = request.get_json()
    if 'description' not in data:
        return jsonify({'errors': ['Validation error: Missing description']}), 400

    if len(data['description']) < 20:
        return jsonify({'errors': ['Validation error: Description must be at least 20 characters long']}), 400

    power.description = data['description']
    db.session.commit()
    
    updated_power_data = {'id': power.id, 'name': power.name, 'description': power.description}
    return jsonify(updated_power_data)

# POST /heropowers
@app.route('/heropowers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    if 'power_id' not in data or 'hero_id' not in data:
        return jsonify({'errors': ['Validation error: Missing power_id or hero_id']}), 400
    
    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])
    
    if hero is None or power is None:
        return jsonify({'errors': ['Validation error: Hero or Power not found']}), 400

    heropower = HeroPower(strength=data.get('strength', 'Average'), hero=hero, power=power)
    db.session.add(heropower)
    db.session.commit()
    
    powers = [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
    hero_data = {'id': hero.id, 'name': hero.name, 'supername': hero.supername, 'powers': powers}  # Use 'supername' instead of 'super_name'
    return jsonify(hero_data), 201

    
if __name__ == '__main__':
    app.run(port=5555)
