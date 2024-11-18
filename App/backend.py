from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__, template_folder="../App/templates", static_folder="../App/static")

# Chemin vers le fichier stocks.json
STOCKS_FILE = os.path.join("App", "stocks.json")

# Charger les données depuis stocks.json
def load_stocks():
    with open(STOCKS_FILE, "r") as file:
        data = json.load(file)
        return data["stocks"]

# Sauvegarder les données dans stocks.json
def save_stocks(stocks):
    with open(STOCKS_FILE, "w") as file:
        json.dump({"stocks": stocks}, file, indent=4)

# Route pour récupérer les stocks
@app.route('/stocks', methods=['GET'])
def get_stocks():
    stocks = load_stocks()
    return jsonify(stocks)

# Route pour ajouter un stock
@app.route('/stocks', methods=['POST'])
def add_stock():
    new_stock = request.json
    stocks = load_stocks()

    # Générer un nouvel ID
    new_stock["id"] = max(stock["id"] for stock in stocks) + 1 if stocks else 1
    stocks.append(new_stock)

    save_stocks(stocks)
    return jsonify(new_stock), 201

# Route pour mettre à jour un stock existant
@app.route('/stocks/<int:id>', methods=['PUT'])
def update_stock(id):
    data = request.json
    stocks = load_stocks()

    stock = next((item for item in stocks if item["id"] == id), None)
    if stock:
        stock.update(data)
        save_stocks(stocks)
        return jsonify(stock)

    return jsonify({"error": "Produit non trouvé"}), 404

# Route pour supprimer un stock
@app.route('/stocks/<int:id>', methods=['DELETE'])
def delete_stock(id):
    stocks = load_stocks()
    stocks = [item for item in stocks if item["id"] != id]
    save_stocks(stocks)
    return jsonify({"message": "Stock supprimé"}), 200

# Route pour récupérer les stocks en alerte
@app.route('/stocks/alerts', methods=['GET'])
def get_alerts():
    stocks = load_stocks()
    alerts = [stock for stock in stocks if stock["quantity"] < stock["threshold"]]
    return jsonify(alerts)

# Route pour charger la page HTML
@app.route('/')
def home():
    return render_template('front.html')

if __name__ == '__main__':
    app.run(debug=True)