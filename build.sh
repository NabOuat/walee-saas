#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "=== Configuration de l'environnement ==="
export PYTHONPATH="${PYTHONPATH}:${PWD}"
echo "PYTHONPATH: $PYTHONPATH"
echo "Current directory: $PWD"
ls -la

echo "=== Upgrade pip, setuptools et wheel ==="
pip install --upgrade pip setuptools wheel

echo "=== Installation des dépendances Python ==="
pip install -r requirements.txt

echo "=== Vérification de l'installation ==="
python -c "import django; print(f'Django version: {django.get_version()}')"
python -c "import walee.settings; print('Settings module found!')"

echo "=== Collecte des fichiers statiques ==="
python manage.py collectstatic --no-input --verbosity 2

# Si vous avez une DB prête, décommentez la ligne suivante
# echo "=== Appliquer les migrations ==="
# python manage.py migrate

echo "=== Build terminé ✅ ==="
