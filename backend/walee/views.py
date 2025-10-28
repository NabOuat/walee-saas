from rest_framework import viewsets
from .models import MaTableSupabase
from .serializers import MaTableSupabaseSerializer

# Un ModelViewSet gère automatiquement les opérations CRUD complètes
class MaTableSupabaseViewSet(viewsets.ModelViewSet):
    # Interroge directement la base de données Supabase via l'ORM Django
    queryset = MaTableSupabase.objects.all() 
    serializer_class = MaTableSupabaseSerializer