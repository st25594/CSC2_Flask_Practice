import json

from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route("/")
def home():

    cart = session.get('cart', {})
    selected_addons = session.get('selected_addons', {})

    flowers, addons = load_data()

    flower_subtotal, addon_subtotal, total = calculate_total(
        cart,
        selected_addons
    )

    return render_template(
        "index.html",
        flowers=flowers,
        addons=addons,
        cart=cart,
        selected_addons=selected_addons,
        flower_subtotal=flower_subtotal,
        addon_subtotal=addon_subtotal,
        total=total
    )
def calculate_total(cart, selected_addons):

    flower_subtotal = sum(
        item['price'] * item['quantity']
        for item in cart.values()
    )

    addon_subtotal = sum(
        price for price in selected_addons.values()
    )

    total = flower_subtotal + addon_subtotal

    return flower_subtotal, addon_subtotal, total
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

@app.route('/remove_from_cart/<item>')
def remove_from_cart(item):
    cart = session.get('cart', {})
    if item in cart:
        del cart[item]
        session['cart'] = cart
        flash(f"{item} removed from cart.")
    else:
        flash(f"{item} not found in cart.")
    return redirect(url_for('home'))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    flower = request.form['flower'] # Get the selected flower name
    quantity = int(request.form['quantity']) # convert quantity to a number
    flowers, addons = load_data() # get flower from file, ignore addon data
    cart = session.get('cart', {}) # get cart from session or start fresh
   
    if flower not in flowers:
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


@app.route('/remove_from_cart/<item>')
@app.route('/select_addon', methods=['POST'])
def select_addon():

    selected_keys = request.form.getlist('addons')

    flowers, addons = load_data()

    selected_addons = {}

    for addon in selected_keys:
        if addon in addons:
            selected_addons[addon] = addons[addon]['price']

    session['selected_addons'] = selected_addons
    session.modified = True

    print(session)

    if selected_addons:
        flash(f"{len(selected_addons)} add-on(s) added to cart.")
    else:
        flash("No add-ons selected.")

    return redirect(url_for('home'))
def remove_from_cart(item):
    cart = session.get('cart', {})
    if item in cart:
        del cart[item]
        session['cart'] = cart
        flash(f"{item} removed from cart.")
    else:
        flash(f"{item} not found in cart.")
    return redirect(url_for('home'))


@app.route('/cancel_order', methods=['POST'])
def cancel_order():

    session.pop('cart', None)
    session.pop('selected_addons', None)

    flash("Order cancelled.")

    return redirect(url_for('home'))


def calculate_total(cart, selected_addons):

    flower_subtotal = sum(
        item['price'] * item['quantity']
        for item in cart.values()
    )

    addon_subtotal = sum(
        price for price in selected_addons.values()
    )

    total = flower_subtotal + addon_subtotal

    return flower_subtotal, addon_subtotal, total



if __name__ == '__main__':
    app.run(debug=True) 