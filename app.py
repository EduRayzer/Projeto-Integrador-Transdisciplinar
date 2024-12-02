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

# Usuários fictícios para login (vamos substituir por um dicionário em memória)
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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Verifica se o nome de usuário já existe
        if username in users:
            flash('Nome de usuário já existe. Tente outro.', 'danger')
            return render_template('signup.html')

        # Verifica se as senhas coincidem
        if password != confirm_password:
            flash('As senhas não coincidem. Tente novamente.', 'danger')
            return render_template('signup.html')

        # Adiciona o novo usuário ao dicionário
        users[username] = password
        flash('Cadastro realizado com sucesso. Agora faça login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

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

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Recupera o carrinho da sessão
    cart = session.get('cart', {})
    
    if str(product_id) in cart:
        # Remove o produto do carrinho se a quantidade for 1
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1  # Decrementa a quantidade
        else:
            del cart[str(product_id)]  # Remove o produto do carrinho
        
        session['cart'] = cart  # Atualiza o carrinho na sessão
    
    return redirect(url_for('cart'))  # Redireciona para a página do carrinho

@app.route('/checkout')
def checkout():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    session.pop('cart', None)  # Limpa o carrinho após a compra
    flash('Compra finalizada com sucesso!', 'success')
    return redirect(url_for('products_view'))

@app.context_processor
def inject_cart_count():
    """Função para injetar o número total de itens no carrinho em todas as páginas"""
    cart = session.get('cart', {})
    cart_count = sum(cart.values())  # Soma as quantidades dos itens no carrinho
    return {'cart_count': cart_count}

if __name__ == '__main__':
    app.run(debug=True)
