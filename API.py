import requests
import streamlit as st
from streamlit_geolocation import streamlit_geolocation

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

st.title("☁️ GÜNCEL HAVA DURUMU ☁️")
st.header("Konum Bilgileriniz")

st.write("Lütfen konumunuzu paylaşmak için aşağıdaki butona tıklayın:")
location = streamlit_geolocation()

if location and location.get('latitude') and location.get('longitude'):
    enlem = location['latitude']
    boylam = location['longitude']
    
    try:
        with st.spinner("Hava durumu bilgileri alınıyor..."):
            geo_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={enlem}&lon={boylam}&accept-language=tr"
            headers = {'User-Agent': 'StreamlitWeatherApp/1.0'}
            geo_response = requests.get(geo_url, headers=headers).json()
            
            address = geo_response.get("address", {})
            sehir = address.get("city") or address.get("town") or address.get("province") or "Bilinmiyor"
            ulke = address.get("country", "Türkiye")
            
            # Hava durumu verilerini Open-Meteo'dan çekelim
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={enlem}&longitude={boylam}&current_weather=true&current_weather_units=true"
            hava_url = requests.get(weather_url).json()
            
            sicaklik = hava_url["current_weather"]["temperature"]
            ruzgar_hizi = hava_url["current_weather"]["windspeed"]
            wmo_kodu = hava_url["current_weather"]["weathercode"]
            derece_isaret = hava_url["current_weather_units"]["temperature"]
            ruzgar_hizi_isaret = hava_url["current_weather_units"]["windspeed"]

        st.info(f"📍 {ulke} / {sehir}")
        
        st.header("Anlık Hava Durumu")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Sıcaklık", value=f"{sicaklik} {derece_isaret}")
        with col2:
            st.metric(label="Rüzgar Hızı", value=f"{ruzgar_hizi} {ruzgar_hizi_isaret}")
            
        st.success(f"Hava Durumu: {get_wmo_text(wmo_kodu)}.")

    except Exception as e:
        st.error("Hava durumu verileri alınırken bir hata oluştu.")
else:
    st.warning("Lütfen yukarıdaki butona basarak konum izni verin.")

if st.button("Yenile"):
    st.rerun()
