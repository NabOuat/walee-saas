// entreprises-api.js

// Nous supposons que cette variable ou fonction est définie dans un fichier global utilitaire
const API_BASE_URL = 'http://localhost:8000/api/'; 

export async function listEntreprises() {
    const response = await fetch(`${API_BASE_URL}/entreprises/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
        }
    });
    
    // Vous pouvez utiliser une fonction utilitaire pour gérer la réponse ici
    if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
    }
    return response.json();
}

// ... exportez d'autres fonctions CRUD ici (createEntreprise, etc.)