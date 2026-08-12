class Position:

    def __init__(
        self,
        direction,
        entry,
        sl,
        tp1,
        tp2,
        tp3,
        risk,
        lot,
    ):

        self.direction = direction

        self.entry = entry

        self.sl = sl

        self.tp1 = tp1
        self.tp2 = tp2
        self.tp3 = tp3

        self.risk = risk

        self.stage = 0

        self.closed = False

        self.result = None
        self.volume1 = 1 / 3
        self.volume2 = 1 / 3
        self.volume3 = 1 / 3

        self.closed_tp1 = False
        self.closed_tp2 = False
        self.closed_tp3 = False
        self.lot = lot