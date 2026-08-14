import time


class CandleWatcher:
    """
    Détecte une nouvelle bougie clôturée.
    """

    def __init__(self):
        self.last_closed_candle = None

    def wait_new_candle(self, downloader):
        while True:
            df = downloader.download_latest()

            if df is None or len(df) < 2:
                print("⏳ Pas assez de données...")
                time.sleep(10)
                continue

            df = df.sort_values("time").reset_index(drop=True)

            # -1 = bougie en formation
            # -2 = dernière bougie clôturée
            closed_candle = df.iloc[-2]["time"]

            if self.last_closed_candle is None:
                self.last_closed_candle = closed_candle
                print(f"🕒 Dernière bougie clôturée : {closed_candle}")
                return

            if closed_candle != self.last_closed_candle:
                self.last_closed_candle = closed_candle
                print(f"✅ Nouvelle bougie clôturée : {closed_candle}")
                return

            print("⏳ Attente de la prochaine bougie clôturée...")
            time.sleep(10)