import urllib.request
import json
import datetime

def is_school_holiday(check_date=None):
    """
    Prüft dynamisch über die OpenHolidays API, ob für das gegebene Datum
    Schulferien in Niedersachsen (DE-NI) vorliegen.
    Gibt ein Tupel (is_holiday: bool, name: str|None) zurück.
    """
    if check_date is None:
        check_date = datetime.date.today()

    valid_from = f"{check_date.year - 1}-12-15"
    valid_to = f"{check_date.year + 1}-01-15"
    url = f"https://openholidaysapi.org/SchoolHolidays?countryIsoCode=DE&subdivisionCode=DE-NI&validFrom={valid_from}&validTo={valid_to}"

    headers = {'User-Agent': 'Mozilla/5.0 (Untis-Scraper; Schulferien-Checker)'}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                holidays = json.loads(response.read().decode('utf-8'))
                for h in holidays:
                    try:
                        start_date = datetime.datetime.strptime(h['startDate'], '%Y-%m-%d').date()
                        end_date = datetime.datetime.strptime(h['endDate'], '%Y-%m-%d').date()
                    except (KeyError, ValueError):
                        continue

                    if start_date <= check_date <= end_date:
                        name_de = "Schulferien"
                        for name_entry in h.get('name', []):
                            if name_entry.get('language') == 'DE':
                                name_de = name_entry.get('text', 'Schulferien')
                                break
                        return True, name_de
    except Exception as e:
        print(f"⚠️ Hinweis: Konnte Ferien-API nicht abfragen ({e}). Fahre normal fort.")

    return False, None

if __name__ == "__main__":
    is_holiday, holiday_name = is_school_holiday()
    if is_holiday:
        print(f"Heute sind Ferien in Niedersachsen: {holiday_name}")
    else:
        print("Heute sind keine Ferien in Niedersachsen.")
