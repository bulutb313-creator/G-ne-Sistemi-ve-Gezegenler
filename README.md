# Jeofizik ve Uzay Bilimleri RAG Chatbotu

### 1 - Projenin Amacı
Bu proje, RAG (Retrieval Augmented Generation) temelli bir chatbot geliştirerek, Dr. Begüm Çıvgın'ın "sistem.pdf" dosyasındaki Jeofizik ve Uzay Bilimleri bilgilerini sorgulamasını sağlamayı amaçlamıştır[cite: 2]. Amaç, yalnızca verilen kaynaktan bilgi çekerek güvenilir ve halüsinasyonsuz cevaplar üretmektir.

### 2 - Veri Seti Hakkında Bilgi
[cite_start]Kullanılan veri seti, Dr. Begüm Çıvgın'ın 2019 tarihli "GENEL JEOFIZIK" ders notlarından ("sistem.pdf") alınmıştır[cite: 72, 101, 140, 154, 169, 197, 237, 282, 309, 350, 383, 411, 441, 479]. İçeriği; [cite_start]Güneş Sistemi, gezegenlerin yapısı, gezegen tanımları, Dünya'nın dış/iç katmanları (Atmosfer, Litosfer, Manto, Çekirdek) ve Jeofiziğin uygulama alanları gibi temel bilimsel konuları kapsamaktadır[cite: 49, 104, 162, 171, 239, 245, 263, 449].

### 4 - Çözüm Mimarisi ve Kullanılan Yöntemler
[cite_start]Proje, RAG mimarisine dayanmaktadır[cite: 2]. Kullanılan temel teknolojiler ve yöntemler:
* [cite_start]**Generation Model (LLM):** Gemini 2.5 Flash [cite: 42] (Sert prompt ve temperature=0.0 ile en kesin cevabı bulmaya zorlanmıştır).
* [cite_start]**Embedding Model:** Google `text-embedding-004` [cite: 43] (Metinleri vektörlere çevirir).
* [cite_start]**Vektör Veritabanı:** FAISS [cite: 43] (Hızlı ve lokal arama için kullanılmıştır).
* [cite_start]**RAG Framework:** LangChain [cite: 44] (Tüm RAG boru hattını oluşturmak için kullanılmıştır).
* [cite_start]**Web Arayüzü:** Streamlit [cite: 25] (Kullanıcı arayüzü ve sunum için).

### 3 - Kodun Çalışma Kılavuzu (Local Ortam)
[cite_start]Kodun çalıştırılabilmesi için gereken adımlar aşağıdadır[cite: 19, 21]:

1.  **Gerekli Kütüphaneler:** Proje dizinindeki `requirements.txt` dosyasını kullanarak tüm bağımlılıkları kurun:
    ```bash
    pip install -r requirements.txt
    ```
2.  **API Anahtarı:** Google Gemini API Anahtarınızı `GEMINI_API_KEY` ortam değişkeni olarak tanımlamanız zorunludur.
3.  **Veri Seti:** Proje verisi olan `sistem.pdf`'in, `app.py` ile aynı klasörde olduğundan emin olun.
4.  **Başlatma:** Web arayüzünü başlatmak için aşağıdaki komutu kullanın:
    ```bash
    streamlit run app.py
    ```

### 5 - Elde Edilen Sonuçlar ve Kabiliyetler
Geliştirilen chatbot, belirlenen kısıtlamalara uyarak yüksek doğrulukla çalışmaktadır:
* [cite_start]**Başarılı Sorgulama:** Yer kabuğu ile manto arasındaki sınırın adı Mohorovicic Süreksizliği (Moho)'dur[cite: 380].
* **Kısıtlı Cevaplama (Halüsinasyon Engelleme):** PDF'te olmayan (örneğin spor veya siyaset) sorulara nazikçe "Üzgünüm, bu bilgiye sağlanan kaynakta yeterince detaylı ulaşılamamaktadır." şeklinde geri dönüş yapar.

### Web Linkiniz

[BURAYA PROJENİZİ YAYINLADIYSANIZ CANLI LİNKİ EKLEMELİSİNİZ.]
