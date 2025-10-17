# 🚀 GÜNEŞ SİSTEMİ VE GEZEGENLER RAG CHATBOTU 🪐

### PROJENİN GENEL ÖZETİ

Bu proje, Akbank GenAI Bootcamp'in temel gereksinimi olan **Retrieval Augmented Generation (RAG)** mimarisi üzerine inşa edilmiştir. Geliştirilen chatbot, bilimsel ve teknik içerikli **`sistem.pdf`** kaynağını kullanarak, kullanıcılardan gelen doğal dil sorgularına yüksek doğruluk ve bağlamsal zenginlikte yanıtlar üretmektedir.

Projenin temel başarısı, bir LLM'in (Gemini 2.5 Flash) erişimini harici, doğrulanmış bir bilgi kaynağı ile sınırlayarak, **halüsinasyon riskini ortadan kaldırmak** ve kaynağa dayalı güvenilir bir bilgi sistemi oluşturmaktır. Çıktı, Streamlit tabanlı bir web arayüzü üzerinden sunulmaktadır.

---

### 1 - GELİŞTİRME ORTAMI (GITHUB & README.MD)

Bu proje, aşağıdaki kriterlere tam uyum sağlamaktadır:
* Projenin kaynak kodu (`.ipynb` veya `.py` uzantılı) GitHub üzerinde sergilenmektedir.
* **README.md** dosyası, projenin Amacı, Veri Seti, Kullanılan Yöntemler ve Elde Edilen Sonuçları detaylı ve profesyonel bir dille özetlemektedir.
* Tüm teknik anlatımlar ve mimari detaylar bu README.md içerisinde yer almaktadır.
* **Web Linki (Deploy Linki)**, README.md'nin en sonunda mutlaka paylaşılmıştır.

---

### 2 - VERİ SETİ HAZIRLAMA

* **Veri Kaynağı:** Dr. Begüm Çıvgın'ın "GENEL JEOFIZIK" ders notları (`sistem.pdf`).
* **İçerik Kapsamı:** Güneş Sistemi'nin oluşum hipotezleri, Gezegenlerin (Merkür'den Neptün'e) hacim, yoğunluk ve yüzey özellikleri, Dünya'nın katmanları (Atmosfer, Hidrosfer) ve Jeofizik detayları (Manto, Çekirdek, Süreksizlikler).
* **Hazırlanış Metodolojisi (Kritik Çözüm):** PDF formatının getirdiği yapısal zorluklar nedeniyle, standart metin yükleyicileri yerine daha sağlam bir yöntem benimsenmiştir:
    1.  **`pdfplumber`** kütüphanesi ile PDF'ten metin çıkarımı manuel olarak yapılmıştır.
    2.  Metin içeriği, **`RecursiveCharacterTextSplitter`** kullanılarak 1000 karakter boyutu ve 200 karakter örtüşme (overlap) ile parçalara (chunks) ayrılmış, böylece bağlamsal bütünlük korunmuştur.

---

### 3 - KODUN ÇALIŞMA KILAVUZU

Projenin yerel veya bulut ortamında (Colab, Kaggle) çalıştırılması için gerekli adımlar:

1.  **Bağımlılıkların Kurulumu (requirements.txt):** Tüm proje bağımlılıklarını içeren `requirements.txt` dosyası kullanılarak kurulum yapılır.
    ```bash
    pip install -r requirements.txt
    ```
2.  **API Anahtarı Tanımlama:** Google AI Studio'dan alınan Gemini API Anahtarı, kodun çalıştırılmasından önce ortam değişkenine tanımlanmalıdır.
    ```bash
    export GEMINI_API_KEY='SİZİN_ANAHTARINIZ'
    ```
3.  **Uygulamanın Başlatılması:** Streamlit web arayüzü, Python betiği (`app.py` veya kullanılan notebook) üzerinden çalıştırılır.
    ```bash
    streamlit run app.py
    ```

---

### 4 - ÇÖZÜM MİMARİNİZ

Kullanılan RAG mimarisi, yüksek performans ve doğru bağlam çekimini garanti etmek üzere optimize edilmiştir:

* **Temel Problem Çözümü:** Proje, Gemini gibi güçlü bir dil modelinin bilgisini genişletmek yerine, onun **bilgi kaynağını kısıtlayarak** ve sadece *`sistem.pdf`*'e dayandırarak güvenilirliğini artırma problemini çözer.
* **Gömme Modeli:** **Google `text-embedding-004`** kullanılmıştır. Bu model, semantic (anlamsal) aramada yüksek alaka düzeyini garanti eder.
* **Vektör Veritabanı:** **ChromaDB**, parçalanan metinlerin vektörlerini depolamak için hızlı ve hafif bir çözüm sunar.
* **Retriever Optimizasyonu (MultiQuery):** Sistemin en kritik zeka katmanıdır. Kullanıcıdan gelen tek bir sorguyu, **LLM'e 3 farklı sorguya dönüştürterek** veritabanında arama yapar. Bu teknik, zorlu ve dolaylı soruların bile bağlamını bulma oranını dramatik şekilde artırır.
* **LLM ve Prompt Mühendisliği:** **Gemini 2.5 Flash ($T=0.2$)** modeli kullanılmış ve Prompt, cevabın **AKICI, LİSTELER KULLANAN ve EN KAPSAMLI ŞEKİLDE DETAYLI** olmasını şart koşmuştur.

---

### 5 - WEB ARAYÜZÜ & PRODUCT KILAVUZU

* **Arayüz Teknolojisi:** Streamlit
* **Çalışma Akışı:** Kullanıcı, canlı linke ulaştıktan sonra sohbet arayüzüne **Güneş Sistemi** veya **Dünya'nın iç yapısı** ile ilgili doğal dil sorularını yazar. Model, anında ve kaynağa dayalı cevaplar üretir.
* **Kabiliyetlerin Testi:** Projenin başarısını doğrulamak için aşağıdaki test senaryoları uygulanmalıdır:
    1.  **Sentez Testi:** "Gezegenleri büyükten küçüğe sırala ve Dünya'nın dış katmanlarını anlat." (Farklı sayfalardaki bilgiyi birleştirme)
    2.  **Doğruluk Testi:** "Atmosferin katmanları nelerdir ve troposferin sıcaklığı nasıl değişir?" (Detaylı bilimsel bilgi çekimi)
    3.  **Halüsinasyon Testi:** "Yerel seçimlerin sonuçları hakkında bilgi verir misin?" (**"Bu konuda elimde yeterli bilgi yok."** yanıtı alınmalıdır.)


### Web Linkiniz

[https://anabelle-monadistic-tomoko.ngrok-free.dev/]









