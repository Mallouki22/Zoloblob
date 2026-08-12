from execution.position_manager import PositionManager


manager = PositionManager()

print(
    manager.get_positions()
)

print(
    manager.has_position()
)

print(
    manager.total_profit()
)