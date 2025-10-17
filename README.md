# 🚀 GÜNEŞ SİSTEMİ VE GEZEGENLER RAG CHATBOTU 🪐

### Projenin Genel Özeti
Bu proje, Akbank GenAI Bootcamp kapsamında, RAG (Retrieval Augmented Generation) mimarisi kullanılarak geliştirilmiş bir chatbot uygulamasıdır. Chatbot, harici bir kaynak olan **sistem.pdf** içeriği hakkında yüksek doğrulukla soruları yanıtlamak üzere tasarlanmıştır.

---

### 1 - Projenin Amacı
Projenin temel amacı, bir yapay zeka modelinin (Gemini) sadece kendisine sağlanan bilimsel metni kullanarak, akıcı, detaylı ve güvenilir cevaplar üretmesini kanıtlamaktır. Model, prompt mühendisliği ile kaynakta olmayan sorulara karşı spesifik bir ret cevabı verecek şekilde kısıtlanmıştır (Halüsinasyon engelleme).

### 2 - Veri Seti Hakkında Bilgi
* **Kaynak:** Dr. Begüm Çıvgın'ın "GENEL JEOFIZIK" ders notları ("sistem.pdf").
* **İçerik Kapsamı:** Güneş Sistemi'nin oluşumu, gezegenlerin özellikleri (Merkür, Venüs, Dünya, Mars, Jüpiter, Satürn, Uranüs, Neptün), Dünya'nın dış katmanları (Atmosfer, Hidrosfer, Biyosfer) ve iç katmanları (Litosfer, Manto, Çekirdek).

### 4 - Çözüm Mimarisi ve Kullanılan Yöntemler
Proje, LangChain çerçevesi kullanılarak RAG mimarisine göre kurulmuştur:
* **Mimari:** Retrieval Augmented Generation (RAG).
* **Generation Model (LLM):** Gemini 2.5 Flash ($T=0.2$ kullanılarak akıcılık ve detaylandırma hedeflenmiştir).
* **Embedding Model:** Google `text-embedding-004` (Güncel ve yüksek performanslı gömme modeli).
* **Vektör Veritabanı:** ChromaDB.
* **Veri İşleme (Kritik Çözüm):** Zorlu PDF formatından metin çıkarma hatalarını aşmak için `pdfplumber` kullanılmış. Metin, detaylı arama için 1000/200 boyutlarında parçalara ayrılmıştır.
* **Arama Optimizasyonu:** Retriever, modelin daha geniş bağlam görmesi ve sentez yapabilmesi için her sorguda 8 en alakalı parçayı (`k=8`) çekecek şekilde ayarlanmıştır.
* **Web Arayüzü:** Streamlit (Sunum kolaylığı için).

### 3 - Kodun Çalışma Kılavuzu (Local Ortam)
Bu projenin yerel bir makinede çalıştırılması için gerekli adımlar:

1.  **Gerekli Kütüphaneler:** Proje klasöründeki `requirements.txt` dosyasını kullanarak tüm bağımlılıkları kurun:
    ```bash
    pip install -r requirements.txt
    ```
2.  **API Anahtarı:** Google AI Studio'dan aldığınız Gemini API Anahtarınızı, kodun çalıştırılmasından önce `GEMINI_API_KEY` ortam değişkenine tanımlayın.
3.  **Başlatma:** Web arayüzünü başlatmak için `app.py` dosyasını çalıştırın:
    ```bash
    streamlit run app.py
    ```

### 5 - Elde Edilen Sonuçlar ve Kabiliyetler (Kanıtlanmış Başarı)
* **RAG Güvenirliği ve Halüsinasyon Engelleme:** Prompt mühendisliği sayesinde, kaynakta bilgi olmadığında model "Bu konuda elimde yeterli bilgi yok." yanıtını vererek **veri dışı uydurma yapmadığını** (halüsinasyonu) kanıtlamıştır.
* **Detaylı Sentez ve Kıyaslama Yeteneği:** Model, retriever tarafından çekilen birden fazla farklı metin parçasını birleştirerek ("Dünya'nın Manto katmanının Kabuk ile farkları nelerdir?" gibi) karmaşık ve karşılaştırmalı sorulara akıcı, bütünleşik cevaplar üretir.
* **Yüksek Doğruluk:** Chatbot, "Yer kabuğu ile manto arasındaki sınıra ne ad verilir?" gibi spesifik sorulara **"Mohorovicic Süreksizliği (Moho)"** yanıtını vererek bilginin doğru çekildiğini kanıtlar.


### Web Linkiniz

[https://anabelle-monadistic-tomoko.ngrok-free.dev/]



