import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime

url_pintuair = "https://poskobanjir.dsdadki.web.id"
url_bekesyong = "https://bpbd.bekasikota.go.id/id/detail/laporan1-harian"

token_bot = ""
chat_id = ""

def send_telegram_message(text):
    telegram_url = f"https://api.telegram.org/bot{token_bot}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    requests.get(telegram_url, params=params)

try:
    while True:
        print("\n===Real-time Pemantauan Debit Air Hulu===")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        waktu_scraping = time.strftime("%Y-%m-%d %H:%M:%S\n")
        report = ""
        report = waktu_scraping
        print(waktu_scraping)
        response_banjir = requests.get(url_pintuair, headers=headers)
        soup_banjir = BeautifulSoup(response_banjir.text, "html.parser")

        rows = soup_banjir.find_all("tr")
        print("Informasi Posko Banjir DSDKI")
        report += "\nInformasi Posko Banjir DSDKI\n"

        for row in rows:
            cols = row.find_all("td")

            if len(cols) >= 4:
                lokasi = cols[1].text.strip()
                tinggi_air = cols[3].text.strip()

                if lokasi in ["Bendung. Cibalok - Gadog (Baru)", "Bendung Katulampa (Hulu)"]:
                    tinggi_air_cm = int(re.search(r'\d+', tinggi_air).group()) if re.search(r'\d+', tinggi_air) else 0
                    #status = "\nKATULAMPA SIAGA 1\n" if lokasi == "Bendung Katulampa (Hulu)" and tinggi_air_cm >= 200 else ""
                    status = ""
                    if lokasi == "Bendung Katulampa (Hulu)":
                        if tinggi_air_cm >= 200:
                            status = "\nKATULAMPA SIAGA 1\n"
                        elif 150 <= tinggi_air_cm < 200:
                            status = "\nKATULAMPA SIAGA 2\n"
                        elif 80 <= tinggi_air_cm < 150:
                            status = "\nKATULAMPA SIAGA 3\n"
                        else:
                            status = ""

                    print(f"{lokasi} | Tinggi Air: {tinggi_air} cm")
                    report += f"{lokasi} | Tinggi Air: {tinggi_air} cm\n"
                    report += (f"{status}")

        print("\n")
        print("Informasi BPBD Bekasi Kota")
        report += "\nInformasi BPBD Bekasi Kota\n"
        response_air = requests.get(url_bekesyong, headers=headers)
        soup_air = BeautifulSoup(response_air.text, "html.parser")

        all_text = soup_air.get_text(separator="\n")

        all_text_cleaned = re.sub(r"\s+", " ", all_text.replace("\xa0", " ")).strip()

        send_alert = False
        alert_message = ""

        match = re.search(r"TINGGI MUKA AIR(.*?)KEJADIAN", all_text_cleaned, re.DOTALL)

        if match:
            result = match.group(1).strip()
            result_fixed = re.sub(r"(\d+\.)", r"\n\1", result).strip()
            print(result_fixed.replace("�", ""))
            report += result_fixed.replace("�", "") + "\n"

        for line in result_fixed.split("\n"):
                if ":" in line:
                    parts = line.split(":")
                    sungai = parts[0].strip()
                    status = parts[1].strip()
                    if status.lower() != "normal":
                        send_alert = True
                        alert_message += f"{sungai} mengalami perubahan status: {status}\n"

        else:
            print("\n[ERROR] Data tinggi muka air tidak ditemukan!")
        if tinggi_air_cm >= 80 or send_alert:
            if send_alert:
                report += "\n[Peringatan] Ada perubahan status sungai!\n" + alert_message
            send_telegram_message(report)
            print(f"[INFO] Laporan dikirim ke Telegram ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
        time.sleep(600)

except KeyboardInterrupt:
    print("\nScraping dihentikan secara manual. Byeee!")
