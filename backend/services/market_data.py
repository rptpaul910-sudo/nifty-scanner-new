import yfinance as yf
import pytz
from datetime import datetime, time as dtime

IST = pytz.timezone("Asia/Kolkata")

NIFTY50 = [
    ("RELIANCE",   "Reliance Industries"),
    ("TCS",        "Tata Consultancy Services"),
    ("HDFCBANK",   "HDFC Bank"),
    ("INFY",       "Infosys"),
    ("ICICIBANK",  "ICICI Bank"),
    ("HINDUNILVR", "Hindustan Unilever"),
    ("SBIN",       "State Bank of India"),
    ("BHARTIARTL", "Bharti Airtel"),
    ("ITC",        "ITC"),
    ("KOTAKBANK",  "Kotak Mahindra Bank"),
    ("LT",         "Larsen & Toubro"),
    ("AXISBANK",   "Axis Bank"),
    ("ASIANPAINT", "Asian Paints"),
    ("MARUTI",     "Maruti Suzuki"),
    ("SUNPHARMA",  "Sun Pharmaceutical"),
    ("TITAN",      "Titan Company"),
    ("BAJFINANCE", "Bajaj Finance"),
    ("WIPRO",      "Wipro"),
    ("ULTRACEMCO", "UltraTech Cement"),
    ("NESTLEIND",  "Nestle India"),
    ("POWERGRID",  "Power Grid Corporation"),
    ("NTPC",       "NTPC"),
    ("TECHM",      "Tech Mahindra"),
    ("HCLTECH",    "HCL Technologies"),
    ("ONGC",       "ONGC"),
    ("TATAMOTORS", "Tata Motors"),
    ("TATASTEEL",  "Tata Steel"),
    ("ADANIENT",   "Adani Enterprises"),
    ("ADANIPORTS", "Adani Ports"),
    ("COALINDIA",  "Coal India"),
    ("DIVISLAB",   "Divi's Laboratories"),
    ("DRREDDY",    "Dr. Reddy's Laboratories"),
    ("EICHERMOT",  "Eicher Motors"),
    ("GRASIM",     "Grasim Industries"),
    ("HDFCLIFE",   "HDFC Life"),
    ("HEROMOTOCO", "Hero MotoCorp"),
    ("HINDALCO",   "Hindalco Industries"),
    ("INDUSINDBK", "IndusInd Bank"),
    ("JSWSTEEL",   "JSW Steel"),
    ("M&M",        "Mahindra & Mahindra"),
    ("CIPLA",      "Cipla"),
    ("BAJAJFINSV", "Bajaj Finserv"),
    ("BAJAJ-AUTO", "Bajaj Auto"),
    ("APOLLOHOSP", "Apollo Hospitals"),
    ("BRITANNIA",  "Britannia Industries"),
    ("SBILIFE",    "SBI Life Insurance"),
    ("TATACONSUM", "Tata Consumer Products"),
    ("UPL",        "UPL"),
    ("BPCL",       "Bharat Petroleum"),
    ("SHREECEM",   "Shree Cement"),
]

TICKERS = [f"{s}.NS" for s, _ in NIFTY50]
NAME_MAP = {f"{s}.NS": n for s, n in NIFTY50}
SYMBOL_MAP = {f"{s}.NS": s for s, _ in NIFTY50}


def get_market_status():
    now = datetime.now(IST)
    is_weekday = now.weekday() < 5
    is_open = is_weekday and dtime(9, 15) <= now.time() <= dtime(15, 30)
    return {
        "is_open": is_open,
        "label": "Market Open" if is_open else "Market Closed",
        "note": None if is_open else "Showing last session data. Market is closed.",
        "checked_at": now.strftime("%Y-%m-%d %H:%M:%S IST")
    }


def fetch_nifty50():
    """
    Fetch all 50 Nifty stocks in one batch call via Yahoo Finance.
    Works 24/7 — returns live data during market hours,
    last session data when market is closed.
    """
    print(f"[Yahoo Finance] Fetching {len(TICKERS)} stocks...")
    try:
        raw = yf.download(
            tickers=TICKERS,
            period="5d",
            interval="1d",
            group_by="ticker",
            auto_adjust=True,
            progress=False,
            threads=True
        )
    except Exception as e:
        print(f"[Yahoo Finance] Download error: {e}")
        return []

    results = []
    for ticker in TICKERS:
        try:
            df = raw[ticker].dropna(how="all") if len(TICKERS) > 1 else raw.dropna(how="all")
            if df.empty or len(df) < 2:
                print(f"[Yahoo Finance] No data for {ticker}")
                continue

            latest     = df.iloc[-1]
            prev       = df.iloc[-2]
            close      = round(float(latest["Close"]), 2)
            prev_close = round(float(prev["Close"]), 2)
            change     = round(close - prev_close, 2)
            change_pct = round((change / prev_close * 100) if prev_close else 0, 2)

            results.append({
                "symbol":         SYMBOL_MAP[ticker],
                "name":           NAME_MAP[ticker],
                "ltp":            close,
                "open":           round(float(latest["Open"]), 2),
                "high":           round(float(latest["High"]), 2),
                "low":            round(float(latest["Low"]), 2),
                "close":          close,
                "prev_close":     prev_close,
                "change":         change,
                "change_percent": change_pct,
                "volume":         int(latest["Volume"])
            })
        except Exception as e:
            print(f"[Yahoo Finance] Error processing {ticker}: {e}")
            continue

    print(f"[Yahoo Finance] Fetched {len(results)}/50 stocks.")
    return results
