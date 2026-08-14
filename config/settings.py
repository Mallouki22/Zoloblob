from pathlib import Path
# ==========================
# PROJECT PATHS
# ==========================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_DIR = PROJECT_ROOT / "datasets"
LOG_DIR = PROJECT_ROOT / "logs"

DATASET_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# ==========================
# DEFAULT MARKET
# ==========================

DEFAULT_SYMBOL = "XAUUSD"

DEFAULT_TIMEFRAME = "M15"

DEFAULT_BARS = 100000

# ==========================
# TRADING
# ==========================

LOT_SIZE = 0.01
MAGIC_NUMBER = 20260717
MAX_OPEN_TRADES = 1
MAX_TRADES_PER_DIRECTION = 1
DEVIATION = 20


# ==========================
# AI
# ==========================

MIN_CONFIDENCE = 0.80

BUY_MIN_CONFIDENCE = 0.80
SELL_MIN_CONFIDENCE = 0.80

HIGH_CONFIDENCE = 0.85


# ==========================
# RISK MANAGEMENT
# ==========================

RISK_PERCENT = 0.005
RISK_REWARD_RATIO = 2.0
ATR_MULTIPLIER = 2

MAX_DAILY_LOSS = 0.01
MAX_CONSECUTIVE_LOSSES = 3

ENABLE_BREAK_EVEN = False
BREAK_EVEN_ATR_TRIGGER = 1.0

ENABLE_TRAILING_STOP = False
TRAILING_ATR_MULTIPLIER = 1.0
# Position management is implemented in both simulation and live monitoring.
# It remains disabled by default so updating the software never changes an
# existing account's behaviour without an explicit configuration choice.
ENABLE_BREAK_EVEN = False
BREAK_EVEN_ATR_TRIGGER = 1.0
ENABLE_TRAILING_STOP = False
TRAILING_ATR_MULTIPLIER = 1.0

# ==========================
# BACKTEST EXECUTION ASSUMPTIONS
# ==========================

# Values are deliberately explicit instead of being inferred from a broker.
# Adjust them to the contract specifications before relying on a simulation.
BACKTEST_POINT_SIZE = 0.01
BACKTEST_FALLBACK_SPREAD_POINTS = 40
BACKTEST_SLIPPAGE_POINTS = 2
BACKTEST_COMMISSION_PER_LOT_ROUND_TURN = 0.0
BACKTEST_CONTRACT_SIZE = 100.0
BACKTEST_FORCE_CLOSE_AT_END = True

# ==========================
# FILTERS
# ==========================

MAX_SPREAD = 40

ALLOW_WEEKEND = False

NEWS_FILTER = True
DATASET_PATH = "datasets/XAUUSD_ML_100k.parquet"
MODEL_PATH = "models/xgboost_gold.pkl"

TP1_RATIO = 1.0
TP2_RATIO = 2.0
TP3_RATIO = 3.0

TP1_VOLUME = 0.25
TP2_VOLUME = 0.25
TP3_VOLUME = 0.50

HIGH_CONFIDENCE = 0.80

MIN_SCORE = 80

TREND_SCORE = 20
MARKET_STRUCTURE_SCORE = 20
BOS_SCORE = 20
LIQUIDITY_SCORE = 20
DXY_SCORE = 20
HTF_SCORE = 20
ATR_SCORE = 20

USE_ADX_FILTER = True
USE_CHOP_FILTER = True

MIN_ADX = 25
MAX_CHOP = 55

ADX_SCORE = 15
CHOP_SCORE = 15

ORDER_BLOCK_SCORE = 20
FVG_SCORE = 15
PD_SCORE = 10