class PositionManager:

    def __init__(self):

        self.positions = []

    def add(self, position):

        self.positions.append(position)

    def remove_closed(self):

        self.positions = [
            p for p in self.positions
            if not p.closed
        ]

    def active(self):

        return [
            p for p in self.positions
            if not p.closed
        ]

    def buy_positions(self):

        return [
            p for p in self.active()
            if p.direction == "BUY"
        ]

    def sell_positions(self):

        return [
            p for p in self.active()
            if p.direction == "SELL"
        ]

    def count(self):

        return len(self.active())