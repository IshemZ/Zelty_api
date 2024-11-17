# Description: Script Python pour récupérer les commandes Zelty et les stocker dans un fichier Excel.
import os
import requests
from dotenv import load_dotenv
import pandas as pd


load_dotenv()

dood_key=os.getenv("API_DOOD_KEY")

# Configurations de base
api_key_dood = dood_key  # Remplacez par votre clé API
BASE_URL = "https://api.zelty.fr/2.9"  # Endpoint des
HEADERS = {
    "Authorization": f"Bearer {api_key_dood}",
    "Content-Type": "application/json"
}

####################### Récupérer les dishes de l'API dood #####################

# Function to fetch dishes
def fetch_dishes():
    response = requests.get(f"{BASE_URL}/catalog/dishes", headers=HEADERS)
    response.raise_for_status()  # Raise error if the request fails
    return response.json()

# Fetch dishes
dishes = fetch_dishes()

# Create a DataFrame from the dishes
dishes_df = pd.DataFrame(dishes)


####################### Récupérer les dishes de l'API dood #####################


# Function to fetch menus
def fetch_menus():
    response = requests.get(f"{BASE_URL}/catalog/menus", headers=HEADERS)
    response.raise_for_status()
    return response.json()

menus = fetch_menus()

menus_df = pd.DataFrame(menus)

# Save to Excel
with pd.ExcelWriter("products_catalog.xlsx") as writer:
    dishes_df.to_excel(writer, sheet_name="Dishes", index=False)
    menus_df.to_excel(writer, sheet_name="Menus", index=False)

print("Product catalog exported to products_catalog.xlsx")