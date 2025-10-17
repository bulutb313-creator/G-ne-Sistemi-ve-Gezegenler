# 🚀 GÜNEŞ SİSTEMİ VE GEZEGENLER RAG CHATBOTU 🪐

<img width="700" height="1600" alt="image" src="https://github.com/user-attachments/assets/a8d3bc2d-12ba-49ba-a1f8-9b903980b637" />


### PROJENİN GENEL ÖZETİ
Bu proje, Akbank GenAI Bootcamp'in zorunlu gereksinimi olan **Retrieval Augmented Generation (RAG)** mimarisi üzerine inşa edilmiştir. Geliştirilen chatbot, harici bir kaynak olan **sistem.pdf** içeriğini kullanarak, yüksek doğruluk ve güvenilirlikte yanıtlar üretmektedir. Projenin temel amacı, bir dil modelini (Gemini) *sadece* kaynağa dayandırarak halüsinasyon riskini ortadan kaldırmaktır.

---

### 1 - GELİŞTİRME ORTAMI (GİTHUB & README.MD)

* **GitHub & Kod Sergileme:** Projenin kodu, aşağıdaki kriterlere uygun bir biçimde GitHub'da sergilenmektedir.
* **Teknik Anlatımlar:** Tüm teknik anlatımlar bu `README.md` dosyasında detaylandırılmıştır.
* **Canlı Bağlantı:** README.md'nin sonunda paylaşılmıştır.

---

### 2 - VERİ SETİ HAZIRLAMA
* **Veri Kaynağı:** Dr. Begüm Çıvgın'ın "GENEL JEOFIZIK" ders notları (`sistem.pdf`) kullanılmıştır.
* **Hazırlanış Metodolojisi (Kritik Çözüm):**
    * **Metin Çıkarımı:** PDF'ten metin çıkarımı, hataları önlemek için daha sağlam olan **`pdfplumber`** ile yapılmıştır.
    * **Parçalama:** Metin, **`RecursiveCharacterTextSplitter`** kullanılarak 1000 karakter boyutu ve 200 karakter örtüşme (overlap) ile parçalara (chunks) ayrılmıştır.

---

### 3 - KODUN ÇALIŞMA KILAVUZU (LOCAL ORTAM)

Bu aşama, kodun başka bir ortamda çalıştırılması için gereken tüm adımları detaylandırır ve profesyonel izolasyonu vurgular:

1.  **Geliştirme Ortamı Kurulumu (İzole Ortam Yaratma):**
    * **Gerekçe:** Proje bağımlılıkları arasındaki çatışmayı önlemek için sanal ortam (Virtual Environment) oluşturulmalıdır.
    * **Komut:** `python -m venv venv` ve ardından ortam etkinleştirilir.
2.  **Bağımlılıkların Kurulumu (`requirements.txt`):**
    * Tüm proje bağımlılıkları, `requirements.txt` dosyası kullanılarak kurulur:
        ```bash
        pip install -r requirements.txt
        ```
3.  **API Anahtarı Tanımlama:**
    * Gemini API Anahtarı, uygulamanın çalıştırılmasından önce ortam değişkenine (`GEMINI_API_KEY`) tanımlanmalıdır.
4.  **Uygulamanın Başlatılması:**
    * Ana Python betiği (`app.py`) çalıştırılarak Streamlit web arayüzü başlatılır:
        ```bash
        streamlit run app.py
        ```

---

### 4 - ÇÖZÜM MİMARİNİZ

* **Mimari:** RAG (Retrieval Augmented Generation).
* **Teknolojiler:** Gemini 2.5 Flash, ChromaDB, MultiQuery Retriever, LangChain.
* **Arama Optimizasyonu (Kapsamlı Sentez):** **MultiQuery Retriever** ve **k=12** ayarları kullanılmıştır. Bu, chatbot'un tek bir sorguyu birden fazla kez aratarak cevabı bulma şansını ve sentez yeteneğini en üst düzeye çıkarır.

---

### 5 - WEB ARAYÜZÜ & PRODUCT KILAVUZU

* **Arayüz Teknolojisi:** Streamlit.
* **Deploy Linki:** Canlı web adresi (`https://...`) bu `README.md`'nin sonunda paylaşılmıştır.
* **Kabiliyetlerin Testi:**
    * **Sentez Testi:** Model, birden fazla kaynaktan bilgi çekip birleştirerek ("Gezegenleri büyükten küçüğe sırala ve Dünya'nın dış katmanlarını anlat.") detaylı cevaplar üretir.
    * **Halüsinasyon Testi:** Kaynak dışı sorgulara , **"Bu konuda elimde yeterli bilgi yok."** yanıtını vererek sistemin güvenilirliği kanıtlanır.




### WEB LİNKİ

[https://anabelle-monadistic-tomoko.ngrok-free.dev/]














