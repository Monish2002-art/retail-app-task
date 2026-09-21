from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simple in-memory product database
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 25.99, "stock": 15},
    {"id": 2, "name": "Mechanical Keyboard", "price": 79.99, "stock": 8},
    {"id": 3, "name": "HD Monitor", "price": 149.99, "stock": 5},
    {"id": 4, "name": "USB-C Hub", "price": 19.99, "stock": 30}
]

cart = []

@app.route('/')
def index():
    return render_template('index.html', products=products, cart=cart)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product and product['stock'] > 0:
        cart_item = next((item for item in cart if item['id'] == product_id), None)
        if cart_item:
            cart_item['quantity'] += 1
        else:
            cart.append({
                "id": product['id'], 
                "name": product['name'], 
                "price": product['price'], 
                "quantity": 1
            })
        product['stock'] -= 1
    return redirect(url_for('index'))

@app.route('/checkout', methods=['POST'])
def checkout():
    cart.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)