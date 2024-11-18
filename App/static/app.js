// Fonction pour récupérer les stocks depuis l'API Flask
function fetchStocks() {
  fetch('/stocks')
    .then(response => {
      if (!response.ok) {
        throw new Error('Erreur lors de la récupération des stocks');
      }
      return response.json();
    })
    .then(data => {
      const tableBody = document.getElementById("stockTable");
      tableBody.innerHTML = ''; // Réinitialiser le tableau avant d'ajouter les lignes

      data.forEach(stock => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${stock.id}</td>
          <td>${stock.name}</td>
          <td>${stock.quantity}</td>
          <td>${stock.unit}</td>
          <td>${stock.threshold}</td>
          <td>
            <button onclick="updateStock(${stock.id})">Modifier</button>
            <button onclick="deleteStock(${stock.id})">Supprimer</button>
          </td>
        `;
        tableBody.appendChild(row); // Ajouter la ligne au tableau
      });
    })
    .catch(error => {
      console.error('Erreur dans fetchStocks:', error);
    });
}

// Fonction pour ajouter un stock
function addStock(event) {
  event.preventDefault(); // Empêcher le rechargement de la page

  const name = document.getElementById("name").value;
  const quantity = parseInt(document.getElementById("quantity").value);
  const unit = document.getElementById("unit").value;
  const threshold = parseInt(document.getElementById("threshold").value);

  fetch('/stocks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name, quantity, unit, threshold })
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Erreur lors de l\'ajout du stock');
      }
      return response.json();
    })
    .then(() => {
      fetchStocks(); // Recharger la liste des stocks
      document.getElementById("addStockForm").reset();
    })
    .catch(error => {
      console.error('Erreur dans addStock:', error);
    });
}

// Fonction pour supprimer un stock
function deleteStock(id) {
  if (confirm('Voulez-vous vraiment supprimer cet élément ?')) {
    fetch(`/stocks/${id}`, {
      method: 'DELETE'
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Erreur lors de la suppression');
        }
        return response.json();
      })
      .then(() => {
        fetchStocks(); // Recharger la liste des stocks
      })
      .catch(error => {
        console.error('Erreur dans deleteStock:', error);
      });
  }
}

// Fonction pour modifier un stock
function updateStock(id) {
  const newQuantity = prompt('Entrez la nouvelle quantité :');
  if (newQuantity !== null) {
    fetch(`/stocks/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ quantity: parseInt(newQuantity) })
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Erreur lors de la mise à jour');
        }
        return response.json();
      })
      .then(() => {
        fetchStocks(); // Recharger la liste des stocks
      })
      .catch(error => {
        console.error('Erreur dans updateStock:', error);
      });
  }
}


// Fonction pour récupérer les alertes depuis l'API Flask
function fetchAlerts() {
  fetch('/stocks/alerts')
    .then(response => {
      if (!response.ok) {
        throw new Error('Erreur lors de la récupération des alertes');
      }
      return response.json();
    })
    .then(alerts => {
      const alertsDiv = document.getElementById("alerts");
      alertsDiv.innerHTML = ''; // Réinitialiser les alertes

      if (alerts.length === 0) {
        alertsDiv.innerHTML = '<p>Aucune alerte.</p>';
      } else {
        alerts.forEach(alert => {
          const alertMessage = `
            <p>
              <strong>${alert.name}</strong> a une quantité critique : 
              ${alert.quantity} ${alert.unit} (seuil : ${alert.threshold} ${alert.unit})
            </p>
          `;
          alertsDiv.innerHTML += alertMessage;
        });
      }
    })
    .catch(error => {
      console.error('Erreur dans fetchAlerts:', error);
    });
}
// Charger les stocks au démarrage
document.addEventListener('DOMContentLoaded', () => {
  fetchStocks(); // Charger les stocks
  fetchAlerts(); // Charger les alertes
});
