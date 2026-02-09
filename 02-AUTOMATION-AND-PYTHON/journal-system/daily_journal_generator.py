#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur automatique de journal de bord quotidien
Auteur: [VOTRE NOM]
Usage: python daily_journal_generator.py --day 1
"""

import os
import argparse
from datetime import datetime, timedelta

# CONFIGURATION (À PERSONNALISER)
START_DATE = "2026-02-09"  # Votre J1 réel
REPO_PATH = os.path.expanduser("~/Bureau/seedrijk-cybersecurity-engineering")  # Adapter chemin

def generate_daily_journal(day_number):
    """Génère un fichier journal pré-rempli"""
    
    # Calcul de la date
    base_date = datetime.strptime(START_DATE, "%Y-%m-%d")
    current_date = base_date + timedelta(days=day_number - 1)
    
    # Formatage dates
    date_str = current_date.strftime("%Y-%m-%d")
    date_fr = current_date.strftime("%d/%m/%Y")
    month_name = current_date.strftime("%B").upper()
    day_names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    day_name = day_names[current_date.weekday()]
    
    # Créer dossier mois si inexistant
    month_folder = f"{REPO_PATH}/01-FOUNDATIONSJOURNAL-DE-BORD/2026-{current_date.strftime('%m')}-{month_name}/"
    os.makedirs(month_folder, exist_ok=True)
    
    # Nom fichier
    filename = f"{month_folder}{date_str}-JOUR-{day_number:02d}.md"
    
    # Template du contenu
    content = f"""# 📅 JOURNAL DE BORD - {day_name.upper()} {date_fr}

**Jour du Challenge** : J{day_number}/100  
**Date** : {date_fr}  
**Météo mentale** : [😊/😐/😓]  
**Énergie** : [🔋🔋🔋🔋🔋] ?/5  
**Heures sommeil** : [?]h

---

## 🎯 OBJECTIFS DU JOUR

### 🎓 Technique
- [ ] **Cours** : [À définir]
- [ ] **Lab** : [À définir]
- [ ] **Livrable** : Day{day_number:02d}/

### 💰 Finance
- [ ] **Lecture** : [15min]
- [ ] **Action** : [Veille/Analyse]

### 📱 Social
- [ ] **Post X** : J{day_number}/100
- [ ] **Post LinkedIn** : [Sujet]

---

## ⏰ PLANNING

### 🌅 Matin (04h00-08h00)

| Heure | Activité | Status | Notes |
|-------|----------|--------|-------|
| 04h00-05h45 | Deep Learning | ⬜ | [Cours J{day_number}] |
| 05h45-06h30 | Finance | ⬜ | - |
| 06h30-08h00 | Sport + Prep | ⬜ | - |

### 🏢 Job (08h00-16h00)
- Automation: [Tâche à scripter]
- Intel: [Observation réseau]

### 🌆 Soir (16h00-01h00)

| Heure | Activité | Status | Notes |
|-------|----------|--------|-------|
| 17h00-19h00 | LAB | ⬜ | [Lab J{day_number}] |
| 20h00-21h30 | Documentation | ⬜ | GitHub |
| 21h30-22h00 | Posts | ⬜ | X + LI |
| 22h00-22h30 | Finance | ⬜ | - |

---

## 📊 BILAN (À remplir ce soir)

**XP gagné** : [?] / 500  
**Commits GitHub** : [?]  
**Posts publiés** : [?] / 2

**Top 3 insights** :
1. [...]
2. [...]
3. [...]

---

**✍️ Généré auto le {datetime.now().strftime("%Y-%m-%d %H:%M")}**
"""
    
    # Écriture fichier
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Journal créé: {filename}")
    print(f"📂 Ouvrir avec: code {filename}")
    
    return filename

def main():
    parser = argparse.ArgumentParser(
        description='Générer journal de bord quotidien',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python daily_journal_generator.py --day 1
  python daily_journal_generator.py --day 10
        """
    )
    parser.add_argument('--day', type=int, required=True, 
                       help='Numéro du jour (1-100)')
    
    args = parser.parse_args()
    
    if args.day < 1 or args.day > 100:
        print("❌ Erreur: Le jour doit être entre 1 et 100")
        return
    
    generate_daily_journal(args.day)

if __name__ == "__main__":
    main()
