# app_name/api_supabase.py
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# import os
# from dotenv import load_dotenv
# load_dotenv()
SUPABASE_URL = "https://<ton-projet>.supabase.co"
SUPABASE_KEY = "<ta-clé-anon-ou-service>"
TABLE = "utilisateurs"

@csrf_exempt
def add_user(request):
    """Endpoint Django pour insérer un utilisateur dans Supabase"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }

            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/{TABLE}",
                headers=headers,
                json=data
            )

            return JsonResponse(response.json(), status=response.status_code, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
