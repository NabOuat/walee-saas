#!/usr/bin/env python3
"""
Script pour générer les icônes PWA pour Walee
Nécessite: pip install Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Tailles d'icônes requises
ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

# Couleurs
BG_COLOR = "#3b82f6"  # Bleu
TEXT_COLOR = "#ffffff"  # Blanc

def create_icon(size, output_path):
    """Créer une icône de la taille spécifiée"""
    # Créer une image avec fond bleu
    img = Image.new('RGB', (size, size), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Ajouter le texte "W" au centre
    try:
        # Essayer d'utiliser une police système
        font_size = int(size * 0.6)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    text = "W"
    
    # Calculer la position pour centrer le texte
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) // 2, (size - text_height) // 2 - bbox[1])
    
    # Dessiner le texte
    draw.text(position, text, fill=TEXT_COLOR, font=font)
    
    # Ajouter un cercle blanc autour (optionnel)
    circle_margin = int(size * 0.1)
    draw.ellipse(
        [circle_margin, circle_margin, size - circle_margin, size - circle_margin],
        outline=TEXT_COLOR,
        width=int(size * 0.02)
    )
    
    # Sauvegarder
    img.save(output_path, 'PNG')
    print(f"✅ Icône créée: {output_path} ({size}x{size})")

def main():
    """Générer toutes les icônes"""
    # Créer le dossier de sortie
    output_dir = os.path.join('frontend', 'static', 'images')
    os.makedirs(output_dir, exist_ok=True)
    
    print("🎨 Génération des icônes PWA pour Walee...")
    print(f"📁 Dossier de sortie: {output_dir}\n")
    
    # Générer chaque taille
    for size in ICON_SIZES:
        output_path = os.path.join(output_dir, f'icon-{size}x{size}.png')
        create_icon(size, output_path)
    
    print(f"\n✅ {len(ICON_SIZES)} icônes générées avec succès!")
    print("\n📝 Prochaines étapes:")
    print("1. Vérifier les icônes dans frontend/static/images/")
    print("2. (Optionnel) Remplacer par un vrai logo avec un outil comme:")
    print("   - https://realfavicongenerator.net/")
    print("   - https://www.pwabuilder.com/imageGenerator")
    print("3. Tester l'installation PWA sur mobile/desktop")

if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print("❌ Erreur: Pillow n'est pas installé")
        print("📦 Installation: pip install Pillow")
        print("\nOu utilisez un outil en ligne:")
        print("- https://realfavicongenerator.net/")
        print("- https://www.pwabuilder.com/imageGenerator")
