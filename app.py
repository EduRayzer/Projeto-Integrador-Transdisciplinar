from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey123'  # Necessário para sessões
Bootstrap(app)

# Produtos fictícios para a loja
products = [
    {'id': 1, 'name': 'Café Gourmet Unifran', 'price': 20.0},
    {'id': 2, 'name': 'Lanche Gourmet Unifran', 'price': 30.0},
    {'id': 3, 'name': 'Jantar Gourmet Unifran', 'price': 40.0}
]

# Usuários fictícios para login
users = {
    'admin': 'unifran',  # username: password
}

# Página inicial que redireciona para o login
@app.route('/')
def home():
    return redirect(url_for('login'))  # Redireciona para a página de login

# Roteiros
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verifica se o usuário e senha são válidos
        if username in users and users[username] == password:
            session['user'] = username  # Salva o usuário na sessão
            return redirect(url_for('products_view'))
        
        flash('Login inválido. Tente novamente.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove o usuário da sessão
    return redirect(url_for('login'))

@app.route('/products')
def products_view():
    if 'user' not in session:
        return redirect(url_for('login'))  # Se não estiver logado, redireciona para o login
    return render_template('products.html', products=products)

@app.route('/cart')
def cart():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Recupera o carrinho da sessão
    cart_items = session.get('cart', {})
    cart_products = []
    total_price = 0
    for product_id, quantity in cart_items.items():
        product = next((prod for prod in products if prod['id'] == int(product_id)), None)
        if product:
            cart_products.append({'product': product, 'quantity': quantity})
            total_price += product['price'] * quantity
    
    return render_template('cart.html', cart_products=cart_products, total_price=total_price)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Adiciona o produto ao carrinho
    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1  # Incrementa a quantidade
    else:
        cart[str(product_id)] = 1  # Adiciona o produto com quantidade 1
    session['cart'] = cart
    
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    session.pop('cart', None)  # Limpa o carrinho após a compra
    flash('Compra finalizada com sucesso!', 'success')
    return redirect(url_for('products_view'))

if __name__ == '__main__':
    app.run(debug=True)
