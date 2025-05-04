import pandas as pd

def Get_battery_and_WLTP_data():

    battery_data = {}
    battery_database = pd.read_excel("Battery database from open source_CellDatabase_v6.xlsx", sheet_name="RAW DATA")
    battery_data = {f"battery_{i}_index": battery_database.iloc[i].tolist() for i in range(348)}  # Adjusted for 348 rows

    WLTP_data = {}
    WLTP_database = pd.read_excel("Battery database from open source_CellDatabase_v6.xlsx", sheet_name="WLTP Acc")
    WLTP_data = {f"WLTP_{i}_index": WLTP_database.iloc[i].tolist() for i in range(1493)}

    return battery_data, WLTP_data