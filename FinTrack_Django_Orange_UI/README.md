# FinTrack — Django Personal Finance Tracker

The interface is in English. The app uses Django, SQLite, user accounts, and daily public exchange-rate APIs.

## 1. Open the correct folder in VS Code
Extract `FinTrack_Django.zip`, then open the folder that directly contains `manage.py` and `requirements.txt`.

In PowerShell, check:
```powershell
Get-ChildItem
```
You must see `manage.py`, `requirements.txt`, `finance`, and `fintrack_project`.

## 2. Set up the environment (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Create database tables
```powershell
python manage.py makemigrations finance
python manage.py migrate
```

## 4. Start the website
```powershell
python manage.py runserver
```
Open http://127.0.0.1:8000/

## 5. Create your personal account
Open http://127.0.0.1:8000/register/ and create an account. The full-name field starts with **Андрей Кочкар**; you can edit it before submitting.

## 6. Create the administrator account
```powershell
python manage.py createsuperuser
```
Then open http://127.0.0.1:8000/admin/

## Included features
- Sign up, sign in, personal account, and sign out
- Each user sees only their own transactions and budgets
- Add and delete income/expense transactions
- Monthly budgets and reports
- Django Admin for users, transactions, budgets, and exchange rates
- USD, EUR and GBP rates from the National Bank of Ukraine
- Bitcoin (BTC) price from CoinGecko
- Rates refresh automatically once per Kyiv calendar day on the first dashboard visit; last saved values remain visible if a provider is temporarily unavailable
- Optional manual rate refresh: `python manage.py update_currency_rates`

**Note:** Daily updates happen when the app is opened that day. If you want updates even when nobody opens the website, schedule `python manage.py update_currency_rates` in Windows Task Scheduler. Rates are informational, not financial advice.
