"""
update_metrics.py - Fusion MD → JSON + totaux globaux

ROLE
----
Automatiser la mise à jour des métriques à partir des fichiers Markdown du journal.

SOURCE DE VÉRITÉ
-----------------
- Les fichiers Markdown sont descriptifs et lisibles par l'humain
- Les fichiers JSON sont autoritatifs pour automatisation et calculs

FICHIERS GÉNÉRÉS
----------------
- XP.json
- Finance.json
- Time.json
"""

import json
import re
from pathlib import Path
from datetime import datetime

# 📍 Chemins (dynamiques, fonctionnent depuis n'importe où)
SCRIPT_DIR = Path(__file__).parent.resolve()  # Dossier du script
REPO_ROOT = SCRIPT_DIR.parent.parent  # Racine du repo (2 niveaux au-dessus)

JOURNAL_DIR = REPO_ROOT / "08-JOURNAL-AND-METRICS" / "2026-02"
METRICS_DIR = SCRIPT_DIR  # Le script est déjà dans METRICS/

METRICS_XP = METRICS_DIR / "XP.json"
METRICS_FINANCE = METRICS_DIR / "Finance.json"
METRICS_TIME = METRICS_DIR / "Time.json"

# 🔹 Initialisation des dictionnaires JSON si fichiers inexistants
def init_json(file_path, default_structure):
    if file_path.exists():
        return json.loads(file_path.read_text())
    else:
        return default_structure

xp_data = init_json(METRICS_XP, {"total_xp": 0, "days": {}, "meta": {}})
finance_data = init_json(METRICS_FINANCE, {"total_finance": 0, "days": {}, "meta": {}})
time_data = init_json(METRICS_TIME, {"total_time": 0.0, "days": {}, "meta": {}})


# 🔹 Parcours des fichiers Markdown
for md_file in JOURNAL_DIR.glob("*.md"):
    content = md_file.read_text()

    day_key = md_file.stem  # ex: 2026-02-09-Day001

    # Extraction des valeurs depuis le Markdown
    xp_match = re.search(r"\*\*XP potentiel bloc 1\*\*\s*:\s*(\d+)", content)
    xp_match2 = re.search(r"\*\*XP potentiel bloc 2\*\*\s*:\s*(\d+)", content)
    xp_val = int(xp_match.group(1)) if xp_match else 0
    xp_val += int(xp_match2.group(1)) if xp_match2 else 0

    finance_match = re.search(r"\*\*Investissement du jour\*\*\s*:\s*(\d+)", content)
    finance_val = int(finance_match.group(1)) if finance_match else 0

    time_match = re.search(r"\*\*Temps total investi aujourd'hui\*\*\s*:\s*~?([\d.]+)h", content)
    time_val = float(time_match.group(1)) if time_match else 0.0

    # 🔹 Mise à jour des fichiers JSON
    xp_data["days"][day_key] = {"xp": xp_val}
    finance_data["days"][day_key] = {"spent": finance_val}
    time_data["days"][day_key] = {"hours": time_val}

# 🔹 Calcul des totaux globaux
xp_data["total_xp"] = sum(d.get("xp", 0) for d in xp_data["days"].values())
finance_data["total_finance"] = sum(d.get("finance", 0) for d in finance_data["days"].values())
time_data["total_time"] = round(sum(d.get("time", 0.0) for d in time_data["days"].values()), 2)


# 🔹 Mise à jour du timestamp
now_iso = datetime.now().isoformat(timespec="minutes")
xp_data["meta"]["last_updated"] = now_iso
finance_data["meta"]["last_updated"] = now_iso
time_data["meta"]["last_updated"] = now_iso

# 🔹 Écriture JSON
METRICS_XP.write_text(json.dumps(xp_data, indent=2))
METRICS_FINANCE.write_text(json.dumps(finance_data, indent=2))
METRICS_TIME.write_text(json.dumps(time_data, indent=2))

print("✅ Metrics updated: XP, Finance, Time")
