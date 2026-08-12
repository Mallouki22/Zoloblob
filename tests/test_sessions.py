from market.sessions import SessionFilter


def main():

    session = SessionFilter()

    print(session.current())

    print(session.is_london_open())

    print(session.is_newyork_open())

    print(session.is_major_session())


if __name__ == "__main__":

    main()