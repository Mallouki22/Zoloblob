from execution.account import AccountManager
from execution.position_manager import PositionManager

def main():

    account = AccountManager()

    print()

    print("Balance :", account.balance())

    print("Equity :", account.equity())

    print("Free Margin :", account.free_margin())

    positions = PositionManager()

    print()

    print("Open positions :", positions.count())


if __name__ == "__main__":
    main()