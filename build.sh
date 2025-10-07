#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "=== Upgrade pip, setuptools et wheel ==="
pip install --upgrade pip setuptools wheel

echo "=== Installation des dépendances Python ==="
pip install -r requirements.txt

echo "=== Collecte des fichiers statiques ==="
python manage.py collectstatic --no-input

# Si vous avez une DB prête, décommentez la ligne suivante
# echo "=== Appliquer les migrations ==="
# python manage.py migrate

echo "=== Build terminé ✅ ==="
