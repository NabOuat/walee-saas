

## Tâche,Méthode,Endpoint Django,Action Supabase GoTrue
Inscription,POST,/api/auth/register/,POST /auth/v1/signup
Connexion,POST,/api/auth/login/,POST /auth/v1/token?grant_type=password
Demande de Reset,POST,/api/auth/reset-password/request/,POST /auth/v1/recover
Déconnexion,POST,/api/auth/logout/,POST /auth/v1/logout
Rafraîchissement,POST,/api/auth/refresh/,POST /auth/v1/token?grant_type=refresh_token
