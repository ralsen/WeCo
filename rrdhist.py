import subprocess
import datetime

def fetch_rrd_to_dict(filename, start="-1h", end="now", cf="AVERAGE"):
    # 1. Daten über Subprocess holen
    cmd = ['rrdtool', 'fetch', filename, cf, '-s', start, '-e', end]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Fehler: {result.stderr}")
        return None

    lines = result.stdout.strip().split('\n')
    
    # 2. Header parsen (Namen der Datenquellen)
    # Die erste Zeile sieht etwa so aus: "         ds_name1 ds_name2"
    header = lines[0].split()
    
    data_list = []
    
    # 3. Datenzeilen parsen (beginnen ab Zeile 3 nach der Leerzeile)
    for line in lines[2:]:
        if not line.strip():
            continue
            
        # Zeile teilen in: "Zeitstempel: Wert1 Wert2 ..."
        timestamp_part, values_part = line.split(':')
        
        timestamp = int(timestamp_part.strip())
        values = values_part.split()
        
        # Dictionary für diesen Zeitpunkt erstellen
        row_dict = {
            "timestamp": timestamp,
            "datetime": datetime.datetime.fromtimestamp(timestamp).isoformat()
        }
        
        # Werte den entsprechenden Headern zuordnen
        for i, val_str in enumerate(values):
            ds_name = header[i]
            # RRD nutzt "nan" für fehlende Daten
            try:
                row_dict[ds_name] = float(val_str.replace(',', '.'))
            except ValueError:
                row_dict[ds_name] = None
        
        data_list.append(row_dict)
    
    return data_list

# Beispielaufruf:
data = fetch_rrd_to_dict('ShellyPStripG4-98A3167B61A0.rrd', start='-1w')
for entry in data:
    print(entry)
     
