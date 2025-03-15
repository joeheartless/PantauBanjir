import requests
import pandas as pd
from datetime import datetime
from tabulate import tabulate
import time

token_bot = "<telegram bot token>"
chat_id = "<chat grup id>"

url = "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm3=32.01.25"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def kirim_laporan():
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Request gagal! Status code: {response.status_code}")
            return

        weather_data = data['data'][0]['cuaca']
        cuaca_list = []
        seen_times = set()

        for group in weather_data:
            for item in group:
                waktu_lokal = item["local_datetime"]
                if waktu_lokal not in seen_times:
                    seen_times.add(waktu_lokal)
                    cuaca_list.append({
                        "Waktu Lokal": waktu_lokal,
                        "Cuaca": item["weather_desc"],
                        "Kecepatan Angin (km/h)": item["ws"],
                        "Tutupan Awan (%)": item["tcc"]
                    })

        df = pd.DataFrame(cuaca_list).drop_duplicates(subset=["Waktu Lokal"]).sort_values("Waktu Lokal")
        df["Waktu Lokal"] = pd.to_datetime(df["Waktu Lokal"])

        now = datetime.now()
        cuaca_sekarang = df.iloc[(df["Waktu Lokal"] - now).abs().argsort()[:1]]
        cuaca_depan = df[df["Waktu Lokal"] > now].head(5)
        df_final = pd.concat([cuaca_sekarang, cuaca_depan]).drop_duplicates(subset=["Waktu Lokal"])

        laporan_cuaca = "*Laporan Cuaca Terkini Area Cisarua (API BMKG)* \n\n"
        for _, row in df_final.iterrows():
            laporan_cuaca += f"*{row['Waktu Lokal'].strftime('%d-%m-%Y %H:%M')}*\n"
            laporan_cuaca += f"*Cuaca:* {row['Cuaca']}\n"
            laporan_cuaca += f"*Kecepatan Angin:* {row['Kecepatan Angin (km/h)']} km/h\n"
            laporan_cuaca += f"*Tutupan Awan:* {row['Tutupan Awan (%)']}%\n"
            laporan_cuaca += "----------------------------------\n"

        telegram_url = f"https://api.telegram.org/bot{token_bot}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": laporan_cuaca,
            "parse_mode": "Markdown"
        }
        response_telegram = requests.post(telegram_url, json=payload)

        if response_telegram.status_code == 200:
            print(f"[INFO] Laporan cuaca dikirim ke Telegram ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
        else:
            print(f"Gagal mengirim ke Telegram! Status: {response_telegram.status_code}")

    except Exception as e:
        print(e)

print("Bot cuaca berjalan... Akan mengirim laporan tiap 2 jam.")

try:
    while True:
        kirim_laporan()
        time.sleep(7200) 
except KeyboardInterrupt:
    print("\nScraping dihentikan secara manual. Byeee!")
