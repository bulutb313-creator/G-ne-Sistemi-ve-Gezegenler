import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma 
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_query import MultiQueryRetriever

# --- RAG ZİNCİRİNİ BAŞLATAN FONKSİYON (Sadece 1 kere çalışır!) ---
# @st.cache_resource, RAG bileşenlerinin Streamlit'in hafızasında kalmasını garanti eder.
@st.cache_resource
def get_rag_chain():
    """Tüm RAG sistemini kurar ve zinciri döndürür."""
    
    # 1. Metin Parçaları (Final Öğretisi)
    # Bu, chatbot'un spresifik ve hassas bilgileri öğrendiği garantili verilerdir.
    texts = [
        Document(page_content="Güneşe en yakın gezegen Merkür'dür. Merkür, güneşe en yakın ve güneş sisteminin en küçük gezegenidir.", metadata={"source": "Tanım Öğretisi"}),
        Document(page_content="Güneşe en uzak gezegen Neptün'dür. Neptün, büyüklük bakımından dördüncü sırada olan ve teleskopla keşfedilmeden önce matematiksel olarak keşfedilmiş bir gezegendir.", metadata={"source": "Tanım Öğretisi"}),
        Document(page_content="Yer kabuğu ile manto arasındaki sınır Mohorovicic Süreksizliği (Moho) olarak adlandırılır.", metadata={"source": "Tanım Öğretisi"}),
        Document(page_content="Güneş sistemindeki gezegenlerin büyükten küçüğe doğru sıralaması: Jüpiter, Satürn, Uranüs, Neptün, Dünya, Venüs, Mars, Merkür.", metadata={"source": "Tanım Öğretisi"}),
        Document(page_content="Mantonun kalınlığı en az 700 km, en fazla 2900 km civarındadır ve Dünya'nın toplam hacminin %84'ünü oluşturur. Dünya'nın en büyük katmanıdır.", metadata={"source": "Tanım Öğretisi"}),
        Document(page_content="Atmosferin temel katmanları (alçaktan yükseğe): Troposfer, Stratosfer, Mezosfer, Termosfer, Ekzosfer.", metadata={"source": "Tanım Öğretisi"}),
    ]
    
    # 2. Embedding Modeli ve Vektör Veritabanı Oluşturma
    embedding_model = GoogleGenerativeAIEmbeddings(model="text-embedding-004") 
    
    try:
        vectorstore = Chroma.from_documents(documents=texts, embedding=embedding_model)
    except Exception as e:
        st.error(f"Vektör veritabanı kurulamadı: {e}")
        return None

    # 3. LLM, Retriever ve Prompt (En Akıllı Ayarlar)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
    
    # Zeki arama: MultiQuery Retriever ile k=8 parça çekiliyor
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 8})
    retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)

    prompt_template = """Sen bir GÜNEŞ SİSTEMİ VE JEOFIZIK UZMANISIN. Sana verilen BAĞLAM'daki tüm bilgileri kullanarak bir cevap SENTEZLE. Cevabını MUTLAKA BAĞLAM'daki bilgilere dayandırarak oluştur. Cevabını AKICI, LİSTELER KULLANARAK ve EN KAPSAMLI ŞEKİLDE DETAYLI yap. Eğer bağlam yoksa, sadece 'Bu konuda elimde yeterli bilgi yok.' de.
        BAĞLAM: {context}
        Soru: {question}
        Cevap:"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT} 
    )
    return qa_chain


# --- STREAMLIT ARAYÜZÜ ANA FONKSİYONU ---

def main():
    st.title("🚀 GÜNEŞ SİSTEMİ VE GEZEGENLER RAG Chatbot 🪐")
    st.caption("Cevaplar sadece 'sistem.pdf'ten alınmıştır. 🛰️")

    # API Anahtarını al ve kontrol et
    if "GEMINI_API_KEY" not in os.environ:
        st.error("Lütfen Gemini API Anahtarınızı giriniz. Anahtar olmadan sistem çalışmaz.")
        key = st.text_input("API Anahtarı:", type="password")
        if key:
            os.environ["GEMINI_API_KEY"] = key
            st.rerun() # Anahtar yüklendikten sonra yeniden başlat
        return
    
    # RAG Zincirini YÜKLE (Cache sayesinde hızlıca yüklenir)
    if "qa_chain" not in st.session_state:
        st.session_state.qa_chain = get_rag_chain()
        if st.session_state.qa_chain is None:
            return

    # Sohbet Geçmişi
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Kullanıcı Girişi
    if prompt := st.chat_input("Güneş Sistemi hakkında bir soru sorun..."):
        
        # Kullanıcı mesajını kaydet
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Chatbot'tan cevap al
        with st.chat_message("assistant"):
            with st.spinner("Cevap aranıyor... 🌑... 🪐... ☄️"):
                try:
                    # RAG zincirini çalıştır
                    answer = st.session_state.qa_chain.run(prompt)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"API hatası oluştu veya zincir kurulamadı. Lütfen API anahtarını kontrol edin: {e}")

if __name__ == "__main__":
    main()
