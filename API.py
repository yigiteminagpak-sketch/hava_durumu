import requests
import streamlit as st

st.set_page_config(page_title="Hava Durumu", page_icon="☁️", layout="centered")

# Görünen ad (Türkçe) -> API'ye gönderilecek ad (İngilizce karakterli) eşleştirmesi
sehirler = {
    "İstanbul": "Istanbul",
    "Ankara": "Ankara",
    "İzmir": "Izmir",
    "Antalya": "Antalya",
    "Bursa": "Bursa",
    "Trabzon": "Trabzon",
    "Adana": "Adana",
    "Gaziantep": "Gaziantep",
    "Konya":"Konya",
    "Şanlıurfa":"Urfa",
    "Kocaeli":"Kocaeli",
    "Mersin":"Mersin",
    "Diyarbakır":"Diyarbakir",
    "Hatay":"Hatay",
    "Manisa":"Manisa",
    "Kayseri":"Kayseri",
    "Samsun":"Samsun",
    "Balıkesir":"Balikesir",
    "Tekirdağ":"Tekirdag",
    "Aydın":"Aydin",
    "Kahramanmaraş":"Kahramanmaras",
    "Sakarya":"Sakarya",
    "Van":"Van",
    "Muğla":"Mugla",
    "Denizli":"Denizli",
    "Eskişehir":"Eskisehir",
    "Mardin":"Mardin",
    "Ordu":"Ordu",
    "Malatya":"Malatya",
    "Afyonkarahisar":"Afyonkarahisar",
    "Erzurum":"Erzurum",
    "Batman":"Batman",
    "Sivas":"Sivas",
    "Adıyaman":"Adiyaman",
    "Tokat":"Tokat",
    "Zonguldak":"Zonguldak",
    "Çanakkale":"Canakkale",
    "Şırnak":"Sirnak",
    "Kütahya":"Kutahya",
    "Osmaniye":"Osmaniye",
    "Çorum":"Corum",
    "Ağrı":"Agri",
    "Giresun":"Giresun",
    "Isparta":"Isparta",
    "Aksaray":"Aksaray",
    "Edirne":"Edirne",
    "Düzce":"Duzce",
    "Yozgat":"Yozgat",
    "Muş":"Mus",
    "Kastamonu":"Kastamonu",
    "Kırklareli":"Kirklereli",
    "Niğde":"Nigde",
    "Uşak":"Usak",
    "Bitlis":"Bitlis",
    "Rize":"Rize",
    "Amasya":"Amasya",
    "Siirt":"Siirt",
    "Bolu":"Bolu",
    "Çankırı":"Cankiri"
}

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

# ARAYÜZ
st.title("☁️ GÜNCEL HAVA DURUMU ☁️")
st.header("Konum Bilgileri")

# Kullanıcı ekranda Türkçe düzgün isimleri görür (İstanbul, İzmir vb.)
secilen_turkce_sehir = st.selectbox("Bir Şehir Seçin:", list(sehirler.keys()))

# API'ye göndermek için İngilizce karakterli karşılığını alıyoruz
api_sehir_adi = sehirler[secilen_turkce_sehir]

if secilen_turkce_sehir:
    try:
        with st.spinner("Seçilen şehrin koordinatları ve hava durumu alınıyor..."):
            # API'ye İngilizce karakterli adı gönderiyoruz
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={api_sehir_adi}&count=1&language=tr&format=json"
            geo_response = requests.get(geo_url).json()
            
            if "results" in geo_response and len(geo_response["results"]) > 0:
                konum = geo_response["results"][0]
                enlem = konum["latitude"]
                boylam = konum["longitude"]
                ulke = konum.get("country", "")
                
                # Bulunan koordinatlarla hava durumu verisini çekiyoruz
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={enlem}&longitude={boylam}&current_weather=true&current_weather_units=true"
                hava_url = requests.get(weather_url).json()
                
                sicaklik = hava_url["current_weather"]["temperature"]
                ruzgar_hizi = hava_url["current_weather"]["windspeed"]
                wmo_kodu = hava_url["current_weather"]["weathercode"]
                derece_isaret = hava_url["current_weather_units"]["temperature"]
                ruzgar_hizi_isaret = hava_url["current_weather_units"]["windspeed"]

                st.info(f"📍 {ulke} / {secilen_turkce_sehir}")
                
                st.header("Anlık Hava Durumu")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Sıcaklık", value=f"{sicaklik} {derece_isaret}")
                with col2:
                    st.metric(label="Rüzgar Hızı", value=f"{ruzgar_hizi} {ruzgar_hizi_isaret}")
                    
                st.success(f"Hava Durumu: {get_wmo_text(wmo_kodu)}.")
            else:
                st.warning("Seçilen şehir için konum bilgisi bulunamadı.")

    except requests.exceptions.RequestException:
        st.title("Bağlantı Hatası!")
        st.error("Bir Sorun Oluştu! Lütfen Daha Sonra Tekrar Deneyiniz.")

if st.button("Yenile"):
    st.rerun()
