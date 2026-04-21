import requests
from config.settings import IDX_API_URL, REQUEST_TIMEOUT

QUARTER_MAP = {
    "Q1": "1",
    "Q2": "2",
    "Q3": "3",
    "Q4": "4",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.idx.co.id/",
}


def _get(url: str, params: dict) -> dict:
    try:
        response = requests.get(
            url, params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"IDX API returned HTTP {exc.response.status_code} for {url}"
        ) from exc
    except requests.RequestException as exc:
        raise RuntimeError(f"Request to IDX API failed: {exc}") from exc


def get_company_profile(symbol: str) -> dict:
    url = f"{IDX_API_URL}/GetCompanyProfile"
    data = _get(url, {"indexCode": symbol.upper()})
    if not data:
        return {}
    item = data[0] if isinstance(data, list) else data
    return {
        "name": item.get("companyName", ""),
        "sector": item.get("sector", ""),
        "sub_sector": item.get("subSector", ""),
        "listing_date": item.get("listingDate", ""),
        "shares_outstanding": item.get("sharesOutstanding", None),
    }


def get_financial_statements(symbol: str, year: int, quarter: str) -> dict:
    quarter_num = QUARTER_MAP.get(quarter.upper(), quarter)
    url = f"{IDX_API_URL}/GetFinancialStatements"
    data = _get(
        url,
        {
            "indexCode": symbol.upper(),
            "year": str(year),
            "quarter": quarter_num,
        },
    )
    if not data:
        return {}
    item = data[0] if isinstance(data, list) else data
    return {
        "revenue": item.get("revenue", None),
        "gross_profit": item.get("grossProfit", None),
        "operating_profit": item.get("operatingProfit", None),
        "net_profit": item.get("netProfit", None),
        "total_assets": item.get("totalAssets", None),
        "total_liabilities": item.get("totalLiabilities", None),
        "total_equity": item.get("totalEquity", None),
        "eps": item.get("eps", None),
        "book_value_per_share": item.get("bookValuePerShare", None),
    }


def get_key_ratios(symbol: str, year: int, quarter: str) -> dict:
    quarter_num = QUARTER_MAP.get(quarter.upper(), quarter)
    url = f"{IDX_API_URL}/GetKeyRatios"
    data = _get(
        url,
        {
            "indexCode": symbol.upper(),
            "year": str(year),
            "quarter": quarter_num,
        },
    )
    if not data:
        return {}
    item = data[0] if isinstance(data, list) else data
    return {
        "roe": item.get("roe", None),
        "roa": item.get("roa", None),
        "npm": item.get("npm", None),
        "der": item.get("der", None),
        "per": item.get("per", None),
        "pbr": item.get("pbr", None),
        "current_ratio": item.get("currentRatio", None),
    }


def scrape_fundamental(symbol: str, year: int, quarter: str) -> dict:
    profile = get_company_profile(symbol)
    financials = get_financial_statements(symbol, year, quarter)
    ratios = get_key_ratios(symbol, year, quarter)
    return {
        "symbol": symbol.upper(),
        "year": year,
        "quarter": quarter.upper(),
        "profile": profile,
        "financials": financials,
        "ratios": ratios,
    }
