import MetaTrader5 as mt5

print("Package version:", mt5.__version__)

print("Initialize sans chemin...")
print(mt5.initialize())
print(mt5.last_error())

mt5.shutdown()