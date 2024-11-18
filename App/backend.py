from flask import Flask, request, jsonify, render_template

# Initialisation de l'application Flask
app = Flask(__name__, template_folder="../App/templates", static_folder="../App/static")  # Spécifier le dossier pour les templates

# Données simulées pour les stocks
stocks = [
    {"id": 1, "name": "Tomates", "quantity": 10, "unit": "kg", "threshold": 5},
    {"id": 2, "name": "Poulet", "quantity": 3, "unit": "kg", "threshold": 2},
]

# Route pour afficher la page HTML
@app.route('/')
def home():
    return render_template('front.html')  # Charger front.html depuis le dossier templates

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

# Route pour supprimer un stock
@app.route('/stocks/<int:id>', methods=['DELETE'])
def delete_stock(id):
    global stocks
    stocks = [item for item in stocks if item["id"] != id]
    return jsonify({"message": "Stock supprimé"}), 200

if __name__ == '__main__':
    app.run(debug=True)