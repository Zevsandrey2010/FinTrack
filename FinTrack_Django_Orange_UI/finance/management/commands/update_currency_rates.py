from django.core.management.base import BaseCommand
from finance.rates import refresh_daily_rates

class Command(BaseCommand):
    help = "Fetch the latest USD, EUR, GBP and Bitcoin exchange rates."

    def handle(self, *args, **options):
        changed = refresh_daily_rates()
        if changed:
            self.stdout.write(self.style.SUCCESS("Currency rates refreshed."))
        else:
            self.stdout.write("Rates are already up to date or providers are temporarily unavailable.")
