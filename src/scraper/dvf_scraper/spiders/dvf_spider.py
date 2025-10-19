import scrapy
from pathlib import Path

class DVFSpider(scrapy.Spider):
    name = "dvf_spider"
    start_urls = ["https://www.data.gouv.fr/api/1/datasets/r/4d741143-8331-4b59-95c2-3b24a7bdbe3c"]

    def parse(self, response):
        # On sauvegarde directement l’URL (le lien vers le fichier ZIP)
        latest_zip = self.start_urls[0]

        output_file = Path(__file__).resolve().parents[3] / "data" / "latest_url.txt"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(latest_zip)

        self.log(f"✅ Lien DVF sauvegardé : {latest_zip}")
