"""
Candle Watcher

Détecte l'arrivée d'une nouvelle bougie.
"""

import time


class CandleWatcher:

    def __init__(self):

        self.last_candle = None


    def wait_new_candle(self, downloader):

        while True:

            df = downloader.download_latest()

            current = df.iloc[-1]["time"]

            if self.last_candle is None:

                self.last_candle = current

                print(f"🕒 Bougie actuelle : {current}")

                return

            if current != self.last_candle:

                self.last_candle = current

                print(f"✅ Nouvelle bougie : {current}")

                return

            print("⏳ Attente de la prochaine bougie...")

            time.sleep(10)