"""
Trading Engine

Cerveau du bot de trading.
"""

import time
from bot.candle_watcher import CandleWatcher
from execution.position_manager import PositionManager
from execution.trade_executor import TradeExecutor
from execution.positions_monitor import PositionMonitor
from data.market_data import MarketDataManager
from data.downloader import DataDownloader
from config.settings import DEFAULT_SYMBOL
from utils.statistics import TradingStatistics
class TradingEngine:

    def __init__(
        self,
        predictor,
        order_manager,
        risk_manager
    ):

        self.predictor = predictor
        self.order_manager = order_manager
        self.risk_manager = risk_manager

        self.running = False
        self.watcher = CandleWatcher()

        self.position_manager = PositionManager()
        self.executor = TradeExecutor(
            order_manager=self.order_manager,
            position_manager=self.position_manager,
            risk_manager=self.risk_manager
        )
        self.position_monitor = PositionMonitor(self.position_manager)
        self.market = MarketDataManager()
        self.market.initialize()
        self.downloader = DataDownloader()
        self.symbol = self.order_manager.client.find_symbol(
            DEFAULT_SYMBOL
        )
        self.statistics = TradingStatistics()
    def start(self):

        self.running = True

        print("🚀 Trading Engine démarré")

        while self.running:

            try:

                self.watcher.wait_new_candle(
                self.downloader
                )

                self.loop()

            except Exception as e:

                print(f"Erreur : {e}")

            time.sleep(5)

    def stop(self):

        self.running = False

        print("🛑 Trading Engine arrêté")

    def show_prediction(
        self,
        prediction
    ):

        print("\n===== PREDICTION =====")

        print("Signal      :", prediction["signal"])

        print(
            "Confidence  :",
            round(prediction["confidence"], 3)
        )

        print("ATR         :", prediction["atr"])

        print("Close       :", prediction["price"])

        print("Time        :", prediction["time"])
    
    def loop(self):

        df = self.market.update()

        prediction = self.predictor.predict(df)
        prediction["market"] = df

        # The ATR comes from the same shared feature pipeline as the signal.
        self.position_monitor.update({self.symbol: prediction["atr"]})
        
        self.show_prediction(prediction)
        self.statistics.add_prediction(
            prediction["signal"]
        )
        opened = self.executor.execute(
            prediction,
            self.symbol
        )

        if opened:

            self.statistics.add_trade()

        else:

            self.statistics.add_refused()

        self.statistics.show()
