# 🚀 GÜNEŞ SİSTEMİ VE GEZEGENLER RAG CHATBOTU 🪐

### Projenin Genel Özeti
Bu proje, Akbank GenAI Bootcamp kapsamında, RAG (Retrieval Augmented Generation) mimarisi kullanılarak geliştirilmiş bir chatbot uygulamasıdır. Chatbot, harici bir kaynak olan **sistem.pdf** içeriği hakkında soruları yanıtlamak üzere tasarlanmıştır.

### 1 - Projenin Amacı
Projenin temel amacı, bir yapay zeka modelinin (Gemini) sadece kendisine sağlanan bilimsel metni kullanarak, akıcı, detaylı ve güvenilir cevaplar üretmesini kanıtlamaktır. Model, kaynakta olmayan sorulara karşı "Bu konuda elimde yeterli bilgi yok." yanıtını verecek şekilde kısıtlanmıştır (Halüsinasyon engelleme).

### 2 - Veri Seti Hakkında Bilgi
Kullanılan veri seti, Dr. Begüm Çıvgın'ın "GENEL JEOFIZIK" ders notlarından alınmıştır. İçeriği; Güneş Sistemi, gezegenlerin oluşumu ve özellikleri, Dünya'nın dış katmanları (Atmosfer, Hidrosfer, Biyosfer) ve iç katmanları (Litosfer, Manto, Çekirdek) gibi Jeofizik konularını kapsamaktadır.

### 4 - Çözüm Mimarisi ve Kullanılan Yöntemler
Proje, RAG mimarisine göre kurulmuştur:
* **Generation Model (LLM):** Gemini 2.5 Flash (Daha akıcı ve detaylı cevaplar için $T=0.2$ kullanılmıştır).
* **Embedding Model:** Google `text-embedding-004`.
* **Vektör Veritabanı:** ChromaDB.
* **RAG Framework:** LangChain.
* **Veri İşleme:** `pdfplumber` ile PDF metinleri çıkarılmış ve hataları önlemek için sağlam (`robust`) parçalama teknikleri kullanılmıştır.
* **Web Arayüzü:** Streamlit (Emojilerle zenginleştirilmiştir).

### 3 - Kodun Çalışma Kılavuzu (Local Ortam)
Bu projenin yerel bir makinede çalıştırılması için gerekli adımlar:

1.  **Gerekli Kütüphaneler:** Proje klasöründeki `requirements.txt` dosyasını kullanarak tüm bağımlılıkları kurun:
    ```bash
    pip install -r requirements.txt
    ```
2.  **API Anahtarı:** Google AI Studio'dan aldığınız Gemini API Anahtarınızı `GEMINI_API_KEY` ortam değişkenine tanımlayın.
3.  **Başlatma:** Web arayüzünü başlatmak için `app.py` dosyasını çalıştırın:
    ```bash
    streamlit run app.py
    ```

### 5 - Elde Edilen Sonuçlar ve Kabiliyetler
* **Yüksek Doğruluk:** Chatbot, "Yer kabuğu ile manto arasındaki sınıra ne ad verilir?" gibi sorulara **"Mohorovicic Süreksizliği (Moho)"** yanıtını vermektedir.
* **Sentez Yeteneği:** Farklı konulardaki bilgileri birleştirerek (örneğin Manto ve Çekirdek karşılaştırması) detaylı ve akıcı cevaplar verebilmektedir.
* **Kısıtlı Cevaplama:** Kaynakta bilgi olmadığında "Bu konuda elimde yeterli bilgi yok." şeklinde net bir geri dönüş yapar.

### Web Linkiniz
[BURAYA, NGROK İLE ALDIĞINIZ CANLI CHATBOT ADRESİNİ YAPIŞTIRMALISINIZ.]