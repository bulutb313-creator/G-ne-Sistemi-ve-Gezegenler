# 🚀 GÜNEŞ SİSTEMİ VE GEZEGENLER RAG CHATBOTU 🪐

### PROJENİN GENEL ÖZETİ
Bu proje, Akbank GenAI Bootcamp'in temel gereksinimi olan **Retrieval Augmented Generation (RAG)** mimarisi üzerine inşa edilmiştir. Geliştirilen chatbot, bilimsel bir kaynak olan **sistem.pdf** içeriğini kullanarak, kullanıcılardan gelen sorgulara yüksek doğruluk ve bağlamsal zenginlikte yanıtlar üretmektedir. Projenin temel başarısı, bir dil modelini (Gemini) *sadece* kaynağa dayandırarak halüsinasyon riskini ortadan kaldırmasıdır.

---

### 1 - GELİŞTİRME ORTAMI (GİTHUB & README.MD) 

Bu kriter, kodun sergilenebilirliğini ve erişilebilirliğini garanti eder:

* **GitHub Reposu:** Tüm proje dosyaları (`app.py`, `requirements.txt`, `sistem.pdf`) GitHub üzerinde sergilenmektedir.
* **Teknik Anlatımlar:** Tüm teknik mimari, Python dosyanızda yorum satırları içerisinde  ve bu `README.md` dosyasında detaylandırılmıştır.
* **README.md İçeriği:** Projenin amacı , veri seti hakkında bilgi , kullanılan yöntemler ve elde edilen sonuçlar  özetlenmiştir.
* **Canlı Bağlantı:** **Web Linki (Deploy Linki)**, README.md'nin sonunda mutlaka paylaşılmıştır.

---

### 2 - VERİ SETİ HAZIRLAMA 

* **Veri Kaynağı:** Dr. Begüm Çıvgın'ın "GENEL JEOFIZIK" ders notları olan hazır bir veri seti (`sistem.pdf`) kullanılmıştır.
* **İçerik Kapsamı:** Güneş Sistemi'nin oluşumu, gezegen özellikleri, Dünya'nın katmanları (Atmosfer, Manto, Çekirdek) gibi Jeofizik konularını içerir.
* **Hazırlanış Metodolojisi (Kritik Çözüm):** PDF formatının getirdiği yapısal zorluklar nedeniyle, standart metin yükleyicileri başarısız olmuştur. Bu durum, **`pdfplumber`** ile manuel metin çıkarımını ve ardından **`RecursiveCharacterTextSplitter`** ile parçalama tekniğini zorunlu kılmıştır. Bu sayede, tüm metin (yaklaşık 41 parça) başarıyla işlenmiştir.

---

### 3 - KODUN ÇALIŞMA KILAVUZU (LOCAL ORTAM) 

Bu aşama, kodun başka bir ortamda çalıştırılması için gereken tüm adımları detaylandırır.

1.  **Geliştirme Ortamı Kurulumu:**
    * Sanal ortam (Virtual Environment) kurulumu gereklidir.
2.  **Bağımlılıkların Kurulumu (`requirements.txt`):**
    * Tüm proje bağımlılıkları, `requirements.txt` dosyası kullanılarak tek komutla kurulur:
        ```bash
        pip install -r requirements.txt
        ```
3.  **API Anahtarı Tanımlama:**
    * Google Gemini API Anahtarı, uygulamanın kod yürütülmesinden önce ortam değişkenine tanımlanmalıdır.
4.  **Uygulamanın Başlatılması:**
    * Ana Python betiği (`app.py`) çalıştırılarak Streamlit web arayüzü başlatılır:
        ```bash
        streamlit run app.py
        ```

---

### 4 - ÇÖZÜM MİMARİNİZ 

Projenin RAG mimarisi, yüksek performans ve doğru bağlam çekimini garanti etmek üzere tasarlanmıştır:

* **Mimari:** RAG (Retrieval Augmented Generation).
* **Çözülen Problem:** LLM'in genel bilgi yerine, sadece `sistem.pdf`'teki veriyi kullanmasını sağlayarak bilginin güvenilirliğini artırma problemi çözülmüştür.
* **Teknolojiler:** Gemini 2.5 Flash, ChromaDB, MultiQuery Retriever, LangChain.
* **Arama Optimizasyonu:** **MultiQuery Retriever** ve **k=12** ayarları kullanılmıştır. Bu, chatbot'un tek bir sorguyu birden fazla kez aratarak cevabı bulma şansını en üst düzeye çıkarır.

---

### 5 - WEB ARAYÜZÜ & PRODUCT KILAVUZU 

* **Arayüz Teknolojisi:** Streamlit.
* **Deploy Linki:** Canlı web adresi (`https://...`) bu `README.md`'nin sonunda paylaşılmıştır.
* **Çalışma Akışı:** Kullanıcı, arayüze ulaştıktan sonra sorularını iletir. **Canlı linkte bizi nasıl bir çalışma akışının beklediği** bu bölümün detaylarında yer alır.
* **Kabiliyetlerin Testi:** Projenin kabiliyetleri, aşağıdaki test senaryoları ile doğrulanabilir:
    1.  **Sentez Testi:** Model, birden fazla kaynaktan bilgi çekip birleştirerek ("Gezegenleri büyükten küçüğe sırala ve Dünya'nın dış katmanlarını anlat.") detaylı cevaplar üretir.
    2.  **Halüsinasyon Testi:** Kaynak dışı sorgulara ("Yerel seçimlerin sonuçları..."), **"Bu konuda elimde yeterli bilgi yok."** yanıtını vererek sistemin güvenilirliği kanıtlanır.


### Web Linkiniz

[https://anabelle-monadistic-tomoko.ngrok-free.dev/]










