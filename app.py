from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/checkout')
def checkout():
    return render_template('invoice.html')

if __name__ == '__main__':
    app.run(debug=True)
    {% if cart%}
        <ul>
        {% for item, details in cart %}
            <li>{{ item }} - Quantity: {{'%.2f' % details['quantity'] }} x ${{ details ['price] }}= ${{ '%.2f' % details['quantity'] * details['price'] }}</li>
        </ul>
        {% endfor %}
        </ul>
        {% else %}
            <p>Your cart is empty.</p>
        {% endif %}