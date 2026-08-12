"""
Trading Sessions
"""

from datetime import datetime, timezone


class SessionFilter:

    def __init__(self):

        self.sessions = {

            "ASIA": (0, 8),

            "LONDON": (7, 16),

            "NEW_YORK": (13, 22),
        }

    def current(self):

        hour = datetime.now(timezone.utc).hour

        active = []

        for name, (start, end) in self.sessions.items():

            if start <= hour < end:

                active.append(name)

        return active

    def is_london_open(self):

        return "LONDON" in self.current()

    def is_newyork_open(self):

        return "NEW_YORK" in self.current()

    def is_major_session(self):

        sessions = self.current()

        return (
            "LONDON" in sessions
            or
            "NEW_YORK" in sessions
        )