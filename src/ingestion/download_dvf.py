import requests
import os
from pathlib import Path
import zipfile

def download_latest_dvf():
    url_file = Path(__file__).resolve().parents[1] / "data" / "latest_url.txt"
    url = url_file.read_text().strip()
    print(f"Lecture du lien depuis {url_file}...")
    if not url_file.exists():
        print("❌ Aucun lien trouvé. Lance d'abord le spider Scrapy.")
        return

    url = url_file.read_text().strip()
    output_dir = Path(__file__).resolve().parents[2] / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    zip_path = output_dir / "valeursfoncieres-latest.zip"
    print(f"Téléchargement depuis {url}...")

    response = requests.get(url, timeout=120)
    if response.status_code == 200:
        with open(zip_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Fichier téléchargé : {zip_path}")
    else:
        print(f"❌ Erreur HTTP {response.status_code}")

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)
    print(f"✅ Fichier extrait dans {output_dir}")

if __name__ == "__main__":
    download_latest_dvf()
