from flask import Flask, request, jsonify, render_template

# Initialisation de l'application Flask
app = Flask(__name__, template_folder="App")  # Spécifier le dossier "App" pour les templates

# Données simulées pour les stocks
stocks = [
    {"id": 1, "name": "Tomates", "quantity": 10, "unit": "kg", "threshold": 5},
    {"id": 2, "name": "Poulet", "quantity": 3, "unit": "kg", "threshold": 2},
]

# Route pour afficher la page HTML
@app.route('/')
def home():
    return render_template('front.html')  # Charger "front.html" depuis le dossier App

# Route pour récupérer les stocks
@app.route('/stocks', methods=['GET'])
def get_stocks():
    return jsonify(stocks)

# Route pour ajouter un nouveau stock
@app.route('/stocks', methods=['POST'])
def add_stock():
    new_stock = request.json
    new_stock["id"] = len(stocks) + 1  # Générer un ID unique
    stocks.append(new_stock)
    return jsonify(new_stock), 201

# Route pour mettre à jour un stock existant
@app.route('/stocks/<int:id>', methods=['PUT'])
def update_stock(id):
    data = request.json
    stock = next((item for item in stocks if item["id"] == id), None)
    if stock:
        stock.update(data)
        return jsonify(stock)
    return jsonify({"error": "Produit non trouvé"}), 404

if __name__ == '__main__':
    app.run(debug=True)