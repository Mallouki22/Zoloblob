import os
import MetaTrader5 as mt5

terminal = r"C:\Users\mallo\AppData\Roaming\MetaTrader 5\terminal64.exe"

print("Terminal existe :", os.path.exists(terminal))
print("Version package :", mt5.__version__)

print("\nInitialisation...")

ok = mt5.initialize(path=terminal)

print("initialize :", ok)
print("last_error :", mt5.last_error())

if ok:
    print("terminal_info :", mt5.terminal_info())
    print("version :", mt5.version())
    mt5.shutdown()