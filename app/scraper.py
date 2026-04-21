import requests
from config.settings import REQUEST_TIMEOUT

QUARTER_MAP = {
    "Q1": "TW1",
    "Q2": "TW2",
    "Q3": "TW3",
    "Q4": "TW4",
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
    """Helper function to make GET requests to IDX API"""
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

def get_financial_report(symbol: str, year: int, quarter: str) -> dict:
    """
    Get financial report from IDX API
    
    Args:
        symbol: Stock code (e.g., 'BBRI', 'ASII')
        year: Year of report (e.g., 2024)
        quarter: Quarter (Q1, Q2, Q3, Q4)
    
    Returns:
        dict: Financial report data
    """
    periode = QUARTER_MAP.get(quarter.upper(), "TW1")
    
    url = "https://www.idx.co.id/primary/ListedCompany/GetFinancialReport"
    
    params = {
        "ReportType": None,
        "KodeEmiten": symbol.upper(),
        "Year": year,
        "SortColumn": "KodeEmiten",
        "SortOrder": "asc",
        "EmitenType": None,
        "Periode": periode,
        "indexfrom": 0,
        "pagesize": 100,
    }
    
    try:
        response_data = _get(url, params)
        
        if response_data.get("ResultCount", 0) > 0 and response_data.get("Results"):
            return response_data["Results"][0]
        else:
            raise RuntimeError(f"No financial data found for {symbol} - {year} {periode}")
            
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch financial report: {exc}") from exc

def parse_financial_data(raw_data: dict) -> dict:
    """Parse raw IDX API response into standardized format"""
    return {
        "kode_emiten": raw_data.get("KodeEmiten"),
        "nama_emiten": raw_data.get("NamaEmiten"),
        "periode_laporan": raw_data.get("PeriodeLaporan"),
        "tanggal_laporan": raw_data.get("TanggalLaporan"),
        "revenue": raw_data.get("Revenue"),
        "cost_of_goods_sold": raw_data.get("CostOfGoodsSold"),
        "gross_profit": raw_data.get("GrossProfit"),
        "operating_expense": raw_data.get("OperatingExpense"),
        "operating_profit": raw_data.get("OperatingProfit"),
        "net_profit": raw_data.get("NetProfit"),
        "total_assets": raw_data.get("TotalAssets"),
        "total_liabilities": raw_data.get("TotalLiabilities"),
        "total_equity": raw_data.get("TotalEquity"),
        "eps": raw_data.get("EPS"),
        "book_value_per_share": raw_data.get("BookValuePerShare"),
        "roe": raw_data.get("ROE"),
        "roa": raw_data.get("ROA"),
        "npm": raw_data.get("NPM"),
        "der": raw_data.get("DER"),
        "per": raw_data.get("PER"),
        "pbr": raw_data.get("PBR"),
        "current_ratio": raw_data.get("CurrentRatio"),
    }

def scrape_fundamental(symbol: str, year: int, quarter: str) -> dict:
    """Main function to scrape fundamental data from IDX"""
    raw_data = get_financial_report(symbol, year, quarter)
    parsed_data = parse_financial_data(raw_data)
    
    return {
        "symbol": symbol.upper(),
        "year": year,
        "quarter": quarter.upper(),
        "data": parsed_data,
        "raw_response": raw_data,
    }