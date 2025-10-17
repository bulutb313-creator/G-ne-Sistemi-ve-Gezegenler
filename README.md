### 🚀 GÜNEŞ SİSTEMİ VE GEZEGENLER RAG CHATBOTU 🪐

### Projenin Genel Özeti

Bu proje, Akbank GenAI Bootcamp'in zorunlu kriteri olan RAG (Retrieval Augmented Generation) mimarisini kullanarak geliştirilmiştir. Nihai ürün, bir web arayüzü üzerinden sunulan ve kaynağa bağlılığı esas alan bir soru-cevap asistanıdır. Chatbot, harici, yapısal olarak zorlu bir bilimsel kaynak olan **sistem.pdf** içeriği hakkında yüksek doğrulukla yanıtlar üretmek üzere tasarlanmıştır.

-----

### 1 - Projenin Amacı (Stratejik Hedefler)

Projenin temel stratejik amacı, basit bir LLM (Large Language Model) arayüzü olmaktan öte, **uzman bir bilgi sisteminin** temelini atmaktır.

  * **Kaynak Kontrolü:** Yapay zeka modelini (Gemini) sadece kendisine sağlanan bilimsel metinle sınırlayarak, bilginin kaynağını kontrol altında tutmak ve üretilen cevapların güvenilirliğini maksimize etmek.
  * **Akıcılık ve Güvenilirlik:** Prompt mühendisliği ile modelin çıktısını akıcı, detaylı ve insan konuşmasına yakın tutarken, eş zamanlı olarak halüsinasyon durumunda spesifik bir ret cevabı ile güvenilirliğini korumak.

### 2 - Veri Seti Hakkında Bilgi (Kaynak ve Zorluk Analizi)

  * **Kaynak:** Dr. Begüm Çıvgın'ın "GENEL JEOFIZIK" ders notları ("sistem.pdf").
  * **Kapsam:** Güneş Sistemi'nin oluşum teorileri, gezegenlerin nicel ve nitel özellikleri, Dünya'nın ana katmanlarının (Atmosfer, Hidrosfer, Biyosfer, Litosfer, Manto, Çekirdek) kimyasal ve fiziksel bileşimleri.
  * **Format Zorluğu:** PDF, metin çıkarımını zorlaştıran çeşitli düzen, tablo ve sayfa sonu sorunları içermektedir. Bu, standart RAG yükleyicileri için kritik hatalara yol açmıştır (bkz. Çözüm Mimarisi).

### 4 - Çözüm Mimarisi ve Kullanılan Yöntemler (Teknik Derinlik)

Proje, LangChain çerçevesinde kurulmuş çok katmanlı bir RAG pipeline'ından oluşur:

| Komponent | Kullanılan Teknoloji | Optimizasyon ve Fonksiyonu |
| :---: | :--- | :--- |
| **Mimari** | Retrieval Augmented Generation (RAG) | **Kaynağa dayalı, halüsinasyonsuz cevap üretimi.** |
| **Veri İşleme** | `pdfplumber` ve `RecursiveCharacterTextSplitter` | **Kritik Çözüm:** Standart `PyPDFLoader` hataları nedeniyle `pdfplumber` ile **manuel metin çıkarma** ve ardından `1000/200` boyutlarında, tüm bilgiyi kapsayan sağlam (`robust`) parçalara ayırma. |
| **Gömme (Embedding)** | Google `text-embedding-004` | Metinlerin anlam uzayında temsil edilerek yüksek alaka düzeyinde arama yapılmasını sağlar. |
| **Vektör DB** | ChromaDB | Vektörlerin lokal olarak depolanması ve hızlı arama yapılması. |
| **Arama (Retriever)** | MultiQuery Retriever + `k=12` | Tek bir kullanıcı sorgusu yerine, model tarafından oluşturulan 3 farklı sorgu ile veritabanının aranması (**Çoklu Sorgu Zekası**). Bu, cevabı bulma olasılığını katlar. |
| **Üretim (LLM)** | Gemini 2.5 Flash ($T=0.2$) | Cevap sentezi ve dil üretimi. Düşük sıcaklık (`T=0.2`), çıktının akıcı ancak kaynağa sadık kalmasını sağlar. |
| **Web Arayüzü** | Streamlit | Kodun, minimal CSS ve emojilerle zenginleştirilmiş, etkileşimli bir sohbet arayüzüne dönüştürülmesi. |

### 3 - Kodun Çalışma Kılavuzu (Local Ortam)

Bu projenin yerel bir makinede çalıştırılması için gereken adımlar:

1.  **Gerekli Kütüphaneler:** Proje klasöründeki `requirements.txt` dosyasını kullanarak tüm bağımlılıkları tek seferde kurun:
    ```bash
    pip install -r requirements.txt
    ```
2.  **API Anahtarı Tanımlama:** Google Gemini API Anahtarınızı, kodun çalıştırılmasından önce **`GEMINI_API_KEY`** ortam değişkenine tanımlamanız zorunludur.
3.  **Başlatma:** `app.py` dosyasını çalıştırarak Streamlit arayüzünü başlatın:
    ```bash
    streamlit run app.py
    ```

### 5 - Elde Edilen Sonuçlar ve Kabiliyetler (Kanıtlanmış Başarı)

Bu RAG chatbotu, uygulanan optimizasyonlar sayesinde en zorlu sorulara bile yüksek performansla yanıt verir:

  * **Sentez ve Kıyaslama Yeteneği (İleri Zeka):** Model, **MultiQuery** arama sonuçlarından çekilen 12 farklı metin parçasını birleştirerek ("Dünya'nın Manto katmanının Kabuk ile farkları nelerdir?") gibi karmaşık, çoklu bilgi gerektiren sorulara akıcı, bütünleşik ve karşılaştırmalı cevaplar üretir.
  * **Yüksek Doğruluk ve Kaynak Kontrolü:** Chatbot, "Yer kabuğu ile manto arasındaki sınıra ne ad verilir?" gibi spesifik bilimsel terminoloji sorularına **"Mohorovicic Süreksizliği (Moho)"** yanıtını vererek bilginin doğru ve kesin çekildiğini kanıtlar.
  * **RAG Güvenirliği ve Halüsinasyon Engelleme:** Kaynakta bilgi olmadığında ("Yerel seçimlerin sonuçları hakkında bilgi verir misin?") model, **"Bu konuda elimde yeterli bilgi yok."** yanıtını vererek, projenin temel güvenilirlik kriterini başarıyla yerine getirir.
    

### Web Linkiniz

[https://anabelle-monadistic-tomoko.ngrok-free.dev/]








