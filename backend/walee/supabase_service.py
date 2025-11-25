
import requests
from rest_framework import status
from django.conf import settings # Importation essentielle pour recuperer les variables

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_ANON_KEY = settings.SUPABASE_ANON_KEY

# Importez vos variables d'environnement
# from config import SUPABASE_URL, SUPABASE_ANON_KEY 

def proxy_to_supabase(request_method, endpoint_path, request, data=None):
    """
    Fonction générique pour transmettre une requête (GET, POST, etc.) à Supabase PostgREST.
    """
    # 1. Récupération du jeton (le jeton doit être vérifié par une couche d'Auth DRF, mais on le récupère ici)
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        # Normalement géré par DRF, mais ici pour la résilience
        return {'error': "Token Bearer invalide ou manquant."}, status.HTTP_401_UNAUTHORIZED
    
    access_token = auth_header.split(' ', 1)[1].strip()
    
    # 2. Construction des Headers
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 3. Construction de l'URL
    url = f"{SUPABASE_URL}/rest/v1/{endpoint_path}"
    
    try:
        # 4. Exécution de la Requête
        response = requests.request(
            method=request_method, 
            url=url, 
            headers=headers, 
            json=data, 
            params=request.query_params # Permet de passer les filtres Supabase (?select=...)
        )
        response.raise_for_status() # Lève une exception si le statut est 4xx ou 5xx
        
        return response.json(), status.HTTP_200_OK

    except requests.exceptions.HTTPError as e:
        # 5. Gestion des erreurs (Renvoie le statut réel de Supabase)
        try:
            error_details = response.json()
        except requests.exceptions.JSONDecodeError:
            error_details = {"detail": "Erreur Supabase inconnue ou non-JSON: " + str(e)}

        # Retourne le statut HTTP de l'erreur Supabase (ex: 401, 403, 404)
        return error_details, response.status_code

    except Exception as e:
        # Erreur interne (ex: problème de connexion réseau)
        return {"detail": f"Erreur de proxy interne : {e}"}, status.HTTP_500_INTERNAL_SERVER_ERROR