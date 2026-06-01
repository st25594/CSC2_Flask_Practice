import json

from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def home():
    flowers, addons = load_data()
    return render_template('index.html',flowers=flowers)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/checkout')
def checkout():

    return render_template('invoice.html')


def load_data():
    with open('data/flowers.json') as file:
        flowers = json.load(file)

    with open('data/addons.json') as file:
        addons = json.load(file)

    return flowers, addons
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    flower = request.form['flower'] # Get the selected flower name
    quantity = int(request.form['quantity']) # convert quantity to a number
    flowers, addons = load_data() # get flower from file, ignore addon data
    cart = session.get('cart', {}) # get cart from session or start fresh
   
    if flower not in cart:
       flash ("invalid flower selected")
       return redirect(url_for('home'))
    
    if flower in cart:
        cart[flower] ['quantity'] += quantity # add to existing quantity
    else:
        cart[flower] = {
            'price': flowers[flower] ['price'],
            'quantity': quantity
            
        }
    session['cart'] = cart # update session  
    session.modified = True # force flask to save it
    flash(f"{quantity} {flower}(s) added to cart.")
    return redirect(url_for('home'))
    
    return render_template('invoice.html')  

if __name__ == '__main__':
    app.run(debug=True)
    @app.route('/remove_from_cart/items', )
def remove_from_cart(item):
    cart = session.get('cart', {})
    if item in cart:
        del cart[item]
        session['cart'] = cart
        flash(f"{item} removed from cart.")
    else:
        flash(f"{item} not found in cart.")
    return redirect(url_for('home'))
def calculate_total(cart):
    total = 0
    for item, details in cart.items():
        total = sum(item['price'] * item['quantity'] for item in cart.values())
    return total
@app.route("/")
def home():
    cart = session.get('cart', {})
    flowers, addons = load_data()
    total = calculate_total(cart)
    return render_template("index.html", flowers=flowers,addons=addons, cart=cart, total=total)
