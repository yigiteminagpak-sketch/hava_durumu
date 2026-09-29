import requests
import streamlit as st

st.set_page_config(page_title="Hava Durumu", page_icon="☁️", layout="centered")

wmo_turkce = {
    0: "Açık gökyüzü",
    1: "Genellikle açık",
    2: "Parçalı bulutlu",
    3: "Çok bulutlu / Kapalı",
    45: "Sisli",
    48: "Kırağılı sis",
    51: "Hafif çisenti",
    53: "Orta şiddette çisenti",
    55: "Yoğun çisenti",
    61: "Hafif yağmurlu",
    63: "Orta şiddette yağmurlu",
    65: "Şiddetli yağmurlu",
    71: "Hafif kar yağışlı",
    73: "Orta şiddette kar yağışlı",
    75: "Yoğun kar yağışlı",
    95: "Gök gürültülü fırtına",
}

def get_wmo_text(code):
    return wmo_turkce.get(code, "Bilinmeyen hava durumu")

try:
    with st.spinner("Konum ve hava durumu bilgileri alınıyor..."):
        ip_istegi = requests.get("https://api.ipify.org?format=json").json()
        ip = ip_istegi["ip"]
        
        konum_url = requests.get(f"https://ipwho.is/{ip}").json()
        
        if not konum_url.get("success", True):
            konum_url = requests.get("https://ipwho.is/").json()

        enlem = konum_url["latitude"]
        boylam = konum_url["longitude"]
        
        url = f"https://api.open-meteo.com/v1/forecast?latitude={enlem}&longitude={boylam}&current_weather=true&current_weather_units=true"
        hava_url = requests.get(url).json()
        
        ulke = konum_url.get("country", "Türkiye")
        sehir = konum_url.get("city", "Bilinmiyor")
        
        sicaklik = hava_url["current_weather"]["temperature"]
        ruzgar_hizi = hava_url["current_weather"]["windspeed"]
        wmo_kodu = hava_url["current_weather"]["weathercode"]
        derece_isaret = hava_url["current_weather_units"]["temperature"]
        ruzgar_hizi_isaret = hava_url["current_weather_units"]["windspeed"]

    st.title("☁️GÜNCEL HAVA DURUMU☁️")
    st.header("Konum Bilgileriniz")
    st.info(f"📍 {ulke} / {sehir} (IP: {ip})")
    
    st.header("Anlık Hava Durumu")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Sıcaklık", value=f"{sicaklik} {derece_isaret}")
    with col2:
        st.metric(label="Rüzgar Hızı", value=f"{ruzgar_hizi} {ruzgar_hizi_isaret}")
        
    st.success(f"Hava Durumu: {get_wmo_text(wmo_kodu)}.")

    if st.button("Yenile"):
        st.rerun()

except requests.exceptions.RequestException:
    st.title("Bağlantı Hatası!")
    st.error("Bir Sorun Oluştu! Lütfen Daha Sonra Tekrar Deneyiniz.")
    if st.button("Yenile"):
        st.rerun()