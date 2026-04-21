import json
import os

FILE_DB = "data_ews.json"

def load_data():
    if os.path.exists(FILE_DB):
        with open(FILE_DB, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(FILE_DB, "w") as f:
        json.dump(data, f, indent=4)

def simpan_data(dinas, parameter, indeks, status):
    data = load_data()

    data.append({
        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dinas": dinas,
        "parameter": parameter,
        "indeks": indeks,
        "status": status
    })

    save_data(data)

def ambil_data():
    return pd.DataFrame(load_data())
