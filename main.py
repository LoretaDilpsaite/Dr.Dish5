import requests

def hole_medikation_daten():
    try:
        response = requests.get("http://127.0.0.1:5000/insulin")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return None


def main():
    data = hole_medikation_daten()
    if not data:
        print("Fehler: Daten konnten nicht abgerufen werden.")
        return

    if "error" in data:
        print(f"Fehler: {data['error']}")
    else:
        print(f"Broteinheiten: {data['brot_einheiten']} {data['einheit']}")
        print(f"Berechnete Insulinmenge: {data['insulinmenge']} IE")


if __name__ == "__main__":
    main()
