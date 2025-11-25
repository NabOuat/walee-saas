// entreprises-api.js

// Nous supposons que cette variable ou fonction est définie dans un fichier global utilitaire
const API_BASE_URL = 'http://localhost:8000/api/'; 

async function listEntreprises() {
    const response = await fetch(`${API_BASE_URL}/organisations/`, {
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
/* Crée une nouvelle entreprise */

async function createEntreprise(data) {
    console.log('Données envoyées pour création:', data);
    try {
        const token = localStorage.getItem('access_token');
        const body = data;

        if (!token) {
            return {
                success: false,
                message: 'Non authentifié'
            };
        }

        const response = await fetch(`${API_BASE_URL}/organisations/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });
        const data = await response.json();
        if (!response.ok) {
            return {
                'success': false,
                "message": data.message || `Erreur HTTP: ${response.status}`
            };
        }
        return data;
    } catch (error) {
        return {
            'success': false,
            "message": error || 'Erreur lors de la création de l\'entreprise'
        };
    }
}

async function updateEntreprise(id, data) {
    const response = await fetch(`${API_BASE_URL}/organisations/${id}/`, {
        method: 'PATCH',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
    }
    return response.json();
}

async function deleteEntreprise(id) {
    const response = await fetch(`${API_BASE_URL}/organisations/${id}/`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
        }
    });
    if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
    }
    return true; // Suppression réussie
}