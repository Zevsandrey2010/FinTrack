from django.utils import timezone
from decimal import Decimal
import requests
from .models import DailyRate

NBU_URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

def refresh_daily_rates():
    """Refresh rates once per Kyiv calendar day when the dashboard is opened."""
    today = timezone.localdate()
    existing = {item.code: item for item in DailyRate.objects.all()}
    if all(code in existing and existing[code].fetched_on == today for code in ("USD", "EUR", "GBP", "BTC")):
        return False

    changed = False
    for code, name in (("USD", "US Dollar"), ("EUR", "Euro"), ("GBP", "British Pound")):
        try:
            response = requests.get(
                NBU_URL,
                params={"valcode": code, "date": today.strftime("%Y%m%d"), "json": ""},
                timeout=8,
            )
            response.raise_for_status()
            payload = response.json()
            if payload and "rate" in payload[0]:
                DailyRate.objects.update_or_create(
                    code=code,
                    defaults={
                        "name": name,
                        "rate": Decimal(str(payload[0]["rate"])),
                        "unit": "UAH",
                        "fetched_on": today,
                        "source": "National Bank of Ukraine",
                    },
                )
                changed = True
        except (requests.RequestException, ValueError, KeyError, TypeError):
            # Keep the most recently saved rate if the provider is temporarily unavailable.
            pass

    try:
        response = requests.get(
            COINGECKO_URL,
            params={"ids": "bitcoin", "vs_currencies": "usd"},
            timeout=8,
        )
        response.raise_for_status()
        btc_price = response.json()["bitcoin"]["usd"]
        DailyRate.objects.update_or_create(
            code="BTC",
            defaults={
                "name": "Bitcoin",
                "rate": Decimal(str(btc_price)),
                "unit": "USD",
                "fetched_on": today,
                "source": "CoinGecko",
            },
        )
        changed = True
    except (requests.RequestException, ValueError, KeyError, TypeError):
        pass
    return changed
