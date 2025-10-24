"""
Module Walee Réservations
Gestion des réservations pour hôtels, restaurants, salons, etc.
"""
from .models import Reservation, CreneauHoraire, Disponibilite
from .views import (
    ReservationListView,
    ReservationCreateView,
    ReservationUpdateView,
    ReservationCancelView,
    DisponibiliteView
)

__all__ = [
    'Reservation',
    'CreneauHoraire',
    'Disponibilite',
    'ReservationListView',
    'ReservationCreateView',
    'ReservationUpdateView',
    'ReservationCancelView',
    'DisponibiliteView',
]
