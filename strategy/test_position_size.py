from strategy.position_size import PositionSizer

sizer = PositionSizer()

lot = sizer.calculate(
    symbol="XAUUSD-STD",
    balance=211.02,
    risk_percent=0.01,
    stop_loss_distance=10
)

print("Lot :", lot)