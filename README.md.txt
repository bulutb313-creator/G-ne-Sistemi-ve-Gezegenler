# Jeofizik ve Uzay Bilimleri RAG Chatbotu

### 1 - Projenin Amacı
[cite_start]Bu proje, RAG (Retrieval Augmented Generation) mimarisi kullanarak bir chatbot geliştirmeyi ve bu chatbotun, Dr. Begüm Çıvgın'ın "sistem.pdf" dosyasındaki Jeofizik ve Uzay Bilimleri bilgilerini sorgulamasını sağlamayı amaçlamıştır[cite: 437]. Amaç, yalnızca verilen kaynaktan bilgi çekerek güvenilir ve halüsinasyonsuz cevaplar üretmektir.

### 2 - Veri Seti Hakkında Bilgi
[cite_start]Kullanılan veri seti, Dr. Begüm Çıvgın'ın 2019 tarihli "GENEL JEOFIZIK" ders notlarından ("sistem.pdf") alınmıştır[cite: 28, 57]. İçeriği; [cite_start]Güneş Sistemi, gezegenlerin yapısı, gezegen tanımları, Dünya'nın dış/iç katmanları (Atmosfer, Litosfer, Manto, Çekirdek) ve Jeofiziğin uygulama alanları gibi temel bilimsel konuları kapsamaktadır[cite: 5, 118, 127, 405].

### 4 - Çözüm Mimarisi ve Kullanılan Yöntemler
[cite_start]Proje, RAG mimarisine dayanmaktadır[cite: 437].
* **Generation Model (LLM):** Gemini 2.5 Flash (Sert prompt ve temperature=0.0 ile en kesin cevabı bulmaya zorlanmıştır).
* **Embedding Model:** Google `text-embedding-004` (Metinleri vektörlere çevirir).
* **Vektör Veritabanı:** FAISS (Hızlı ve lokal arama için kullanılmıştır).
* **RAG Framework:** LangChain (Tüm RAG boru hattını oluşturmak için kullanılmıştır).
* **Veri İşleme:** PDF'ten çıkarılan metinler, bilginin dağılmasını engellemek için büyük parçalara (chunk_size=4000) ayrılmıştır.

### 3 - Kodun Çalışma Kılavuzu (Local Ortam)
Kodun çalıştırılabilmesi için gerekenler aşağıdadır:

1.  **Gerekli Kütüphaneler:** Proje dizinindeki `requirements.txt` dosyasını kullanarak tüm bağımlılıkları kurun:
    ```bash
    pip install -r requirements.txt
    ```
2.  **API Anahtarı:** Google Gemini API Anahtarınızı `GEMINI_API_KEY` ortam değişkeni olarak tanımlamanız zorunludur.
3.  **Başlatma:** Web arayüzünü başlatmak için aşağıdaki komutu kullanın:
    ```bash
    streamlit run app.py
    ```

### 5 - Elde Edilen Sonuçlar ve Kabiliyetler
Geliştirilen chatbot, belirlenen kısıtlamalara uyarak yüksek doğrulukla çalışmaktadır:
* [cite_start]**Başarılı Sorgulama:** Yer kabuğu ile manto arasındaki sınırın adı Mohorovicic Süreksizliği (Moho)'dur[cite: 259, 336].
* **Kısıtlı Cevaplama:** PDF'te olmayan (örneğin spor veya siyaset) sorulara nazikçe "Üzgünüm, bu bilgiye sağlanan kaynakta yeterince detaylı ulaşılamamaktadır." şeklinde geri dönüş yapar.

### Web Linkiniz
[BURAYA, EĞER UYGULAMAYI YAYINLARSANIZ (Streamlit Cloud vb.) O CANLI LİNKİ EKLEYİN.]
