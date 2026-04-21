from openai import OpenAI
from config.settings import OPENAI_API_KEY, OPENAI_MODEL


def summarize_fundamental(data: dict) -> str:
    if not OPENAI_API_KEY:
        return "OpenAI API key not configured."

    client = OpenAI(api_key=OPENAI_API_KEY)

    symbol = data.get("symbol", "")
    year = data.get("year", "")
    quarter = data.get("quarter", "")
    profile = data.get("profile", {})
    financials = data.get("financials", {})
    ratios = data.get("ratios", {})

    prompt = f"""
Berikut adalah data fundamental saham {symbol} untuk periode {quarter} {year}:

Profil Perusahaan:
- Nama: {profile.get('name', 'N/A')}
- Sektor: {profile.get('sector', 'N/A')}
- Sub-sektor: {profile.get('sub_sector', 'N/A')}
- Saham Beredar: {profile.get('shares_outstanding', 'N/A')}

Laporan Keuangan:
- Pendapatan: {financials.get('revenue', 'N/A')}
- Laba Kotor: {financials.get('gross_profit', 'N/A')}
- Laba Operasional: {financials.get('operating_profit', 'N/A')}
- Laba Bersih: {financials.get('net_profit', 'N/A')}
- Total Aset: {financials.get('total_assets', 'N/A')}
- Total Liabilitas: {financials.get('total_liabilities', 'N/A')}
- Total Ekuitas: {financials.get('total_equity', 'N/A')}
- EPS: {financials.get('eps', 'N/A')}

Rasio Keuangan:
- ROE: {ratios.get('roe', 'N/A')}
- ROA: {ratios.get('roa', 'N/A')}
- NPM: {ratios.get('npm', 'N/A')}
- DER: {ratios.get('der', 'N/A')}
- PER: {ratios.get('per', 'N/A')}
- PBR: {ratios.get('pbr', 'N/A')}
- Current Ratio: {ratios.get('current_ratio', 'N/A')}

Berikan ringkasan singkat dalam Bahasa Indonesia mengenai kondisi fundamental saham ini, termasuk kekuatan, kelemahan, dan pandangan umum untuk investor ritel.
""".strip()

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Kamu adalah analis saham profesional yang membantu investor ritel "
                    "memahami data fundamental saham Indonesia dengan bahasa yang mudah dipahami."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
