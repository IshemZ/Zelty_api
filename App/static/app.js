function fetchStocks() {
  fetch('/stocks')
    .then(response => {
      if (!response.ok) {
        throw new Error('Erreur lors de la récupération des données');
      }
      return response.json();
    })
    .then(data => {
      console.log("Données récupérées :", data); // Débogage
      const tableBody = document.getElementById("stockTable");
      tableBody.innerHTML = ''; // Vider le tableau avant d'ajouter des lignes

      data.forEach(stock => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${stock.name}</td>
          <td>${stock.quantity}</td>
          <td>${stock.unit}</td>
          <td>${stock.threshold}</td>
          <td>
            <button onclick="updateStock(${stock.id})">Modifier</button>
            <button onclick="deleteStock(${stock.id})">Supprimer</button>
          </td>
        `;
        tableBody.appendChild(row);
      });
    })
    .catch(error => {
      console.error('Erreur dans fetchStocks:', error);
    });
}