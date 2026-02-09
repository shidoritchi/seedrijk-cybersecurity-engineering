"""
update_metrics.py

ROLE
----
Recalculer les métriques globales (XP, temps, finance)
à partir du fichier metrics.json qui est la SOURCE DE VÉRITÉ.

IMPORTANT
---------
- Les fichiers Markdown sont uniquement descriptifs (lecture humaine)
- AUCUNE donnée ne doit être calculée depuis les .md
"""

import json
from pathlib import Path
from datetime import datetime

# 📍 Chemin vers le fichier JSON maître
METRICS_FILE = Path("08-JOURNAL-AND-METRICS/METRICS/metrics.json")

# 🛑 Sécurité : le fichier doit exister
if not METRICS_FILE.exists():
    raise FileNotFoundError("metrics.json not found. Metrics authority is missing.")

# 📥 Chargement des données
data = json.loads(METRICS_FILE.read_text())

# 🔢 Initialisation des totaux
total_xp = 0
total_time = 0.0
total_finance = 0

# 🔁 Parcours de chaque jour enregistré
for day_id, day_data in data.get("days", {}).items():
    total_xp += day_data.get("xp", 0)
    total_time += day_data.get("time_hours", 0)
    total_finance += day_data.get("finance_usd", 0)

# 🧮 Mise à jour des totaux globaux
data["totals"] = {
    "xp": total_xp,
    "time_hours": round(total_time, 2),
    "finance_usd": total_finance
}

# 🕒 Mise à jour du timestamp
data["meta"]["last_updated"] = datetime.now().isoformat(timespec="minutes")

# 💾 Sauvegarde
METRICS_FILE.write_text(json.dumps(data, indent=2))

print("✅ Metrics recalculated from authoritative JSON.")

