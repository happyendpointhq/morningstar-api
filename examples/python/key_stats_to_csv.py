"""Write key statistics for a list of stocks to CSV, one /stock/details call per stock.

    python key_stats_to_csv.py AAPL:xnas MSFT:xnas --out stocks.csv

Values are as Morningstar reports them: ratios as plain numbers, yields and returns in
percent (0.31 means 0.31%, not 31%). Locked premium fields are left empty.
"""

import argparse
import csv

from client import component, get, value

COLUMNS = [
    "ticker", "exchange", "name", "performance_id", "sector", "industry", "style_box",
    "employees", "pe_normalized", "price_to_book", "price_to_sales", "price_to_cash_flow",
    "dividend_yield_trailing_pct", "total_yield_pct", "roe_normalized_pct", "quick_ratio",
    "current_ratio", "shares_outstanding",
]


def own_row(details, section):
    """This stock's row in a ...VsBenchmarks section (the others are competitors)."""
    rows = (component(details, section) or {}).get("dataPoints") or []
    ticker = details["page"]["ticker"]
    return next((r["values"] for r in rows if r["label"] == ticker), {})


def row_for(ticker, exchange):
    details = get("/stock/details", ticker=ticker, exchange=exchange)
    page = details["page"]
    profile = (component(details, "profile") or {}).get("dataPoints") or {}
    stats = (component(details, "keyStatistics") or {}).get("dataPoints") or {}
    trading = (component(details, "tradingInformation") or {}).get("dataPoints") or {}
    valuation = own_row(details, "valuationVsBenchmarks")
    profitability = own_row(details, "profitabilityVsBenchmarks")
    strength = own_row(details, "financialStrengthVsBenchmarks")
    return {
        "ticker": page["ticker"],
        "exchange": page["exchange"],
        "name": page["name"],
        "performance_id": page["performanceID"],
        "sector": value(profile.get("sector")),
        "industry": value(profile.get("industry")),
        "style_box": value(profile.get("stockStyleBox")),
        "employees": value(profile.get("totalEmployees")),
        "pe_normalized": value(valuation.get("priceToEarnings[normalized]")),
        "price_to_book": value(valuation.get("priceToBook")),
        "price_to_sales": value(valuation.get("priceToSales")),
        "price_to_cash_flow": value(valuation.get("priceToCashFlow")),
        "dividend_yield_trailing_pct": value(stats.get("dividendYield[trailing]")),
        "total_yield_pct": value(stats.get("totalYield")),
        "roe_normalized_pct": value(profitability.get("returnOnEquity[normalized]")),
        "quick_ratio": value(strength.get("quickRatio")),
        "current_ratio": value(strength.get("currentRatio")),
        "shares_outstanding": value(trading.get("totalSharesOutstanding")),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stocks", nargs="+", help="TICKER:exchange, for example AAPL:xnas")
    parser.add_argument("--out", default="stocks.csv")
    args = parser.parse_args()

    with open(args.out, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for item in args.stocks:
            ticker, _, exchange = item.partition(":")
            row = row_for(ticker, exchange or "xnas")
            writer.writerow(row)
            print(f"{row['ticker']:<8} {row['name']:<32} P/E {row['pe_normalized']}")
    print(f"Wrote {len(args.stocks)} rows to {args.out}")


if __name__ == "__main__":
    main()
