import requests
import json


URL = "http://192.168.2.5:8080/sendDevInfo"
DATEI = "daten.json"

URL1 = "http://192.168.2.5:8080/sendDevList"
DATEI1 = "devlist.json"

URL2 = "http://192.168.2.5:8080/sendDSInfo"
DATEI2 = "dsinfo.json"

def lade_json(url):
    response = requests.get(url, timeout=10)

    # Fehler werfen wenn HTTP nicht OK
    response.raise_for_status()

    return response.json()


def speichern(daten, dateiname):
    with open(dateiname, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=4, ensure_ascii=False)


def main():
    try:
        daten = lade_json(URL)
        speichern(daten, DATEI)

        print(f"Daten gespeichert in: {DATEI}")
        print(daten)

        daten1 = lade_json(URL1)
        speichern(daten1, DATEI1)

        print(f"Daten gespeichert in: {DATEI1}")
        print(daten1)
        
        daten2 = lade_json(URL2)
        speichern(daten2, DATEI2)

        print(f"Daten gespeichert in: {DATEI2}")
        print(daten2)
        
    except requests.RequestException as e:
        print(f"HTTP-Fehler: {e}")

    except Exception as e:
        print(f"Fehler: {e}")


if __name__ == "__main__":
    main()