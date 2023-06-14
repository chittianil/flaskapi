from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bootcamp_user:bootcamp%402022@10.80.2.22:4213/bootcamp_2022'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Product class/model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)


# Create a product
@app.route('/product', methods=['POST'])
def create_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name=name, description=description, price=price, qty=qty)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product created successfully'})


# Read all products
@app.route('/product', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    result = []
    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'qty': product.qty
        }
        result.append(product_data)

    return jsonify(result)


# Read a single product
@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product:
        return jsonify({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'qty': product.qty
        })
    else:
        return jsonify({'message': 'Product not found'}), 404


# Update a product
@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    product.name = request.json['name']
    product.description = request.json['description']
    product.price = request.json['price']
    product.qty = request.json['qty']
    db.session.commit()

    return jsonify({'message': 'Product updated successfully'})


# Delete a product
@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Product deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)
