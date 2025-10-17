import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma 
from langchain.docstore.document import Document
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter


# --- RAG ZİNCİRİNİ BAŞLATAN FONKSİYON ---
@st.cache_resource
def get_rag_chain():
    """Tüm RAG sistemini kurar ve zinciri döndürür."""
    
    # 1. Manüel Metin Parçaları (Test için kısıtlı set)
    texts = [
        Document(page_content="Güneş sistemindeki en sıcak gezegen: Venüs", metadata={"source": "sistem.pdf"}),
        Document(page_content="Güneş sistemindeki en soğuk gezegen: Uranüs", metadata={"source": "sistem.pdf"}),
        Document(page_content="Yer kabuğu ile manto arasındaki sınıra Mohorovicic Süreksizliği (Moho) denilir.", metadata={"source": "sistem.pdf"}),
        Document(page_content="Jüpiter, Güneş sisteminin en büyük gezegenidir ve 63 uyduya sahiptir.", metadata={"source": "sistem.pdf"}),
        Document(page_content="Mantonun kalınlığı en az 700 km, en fazla 2900 km civarındadır ve Dünya'nın toplam hacminin %84'ünü oluşturur. Dünya'nın en büyük katmanıdır.", metadata={"source": "sistem.pdf"}),
    ]
    
    # 2. Embedding Modeli ve Vektör Veritabanı Oluşturma
    embedding_model = GoogleGenerativeAIEmbeddings(model="text-embedding-004") 
    
    try:
        vectorstore = Chroma.from_documents(documents=texts, embedding=embedding_model)
    except Exception as e:
        st.error(f"Vektör veritabanı kurulamadı: {e}")
        return None

    # 3. LLM, Retriever ve Prompt
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 8}) 

    prompt_template = """Sen bir GÜNEŞ SİSTEMİ VE GEZEGENLER CHATBOTU'sun. Görevin, sana verilen BAĞLAMI (GÜNEŞ SİSTEMİ VE GEZEGENLER HAKKINDAKİ BELGEYİ) kullanarak kullanıcı sorularını AKICI ve MÜMKÜN OLDUĞUNCA detaylıca cevaplamaktır. Cevabını doğal ve açıklayıcı yap.

Eğer cevap BAĞLAM'da yoksa, sadece "Bu konuda elimde yeterli bilgi yok." diye cevap ver. Asla uydurma bilgi verme.

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
    # Başlık ve Emojiler Eklendi
    st.title("🚀 GÜNEŞ SİSTEMİ VE GEZEGENLER RAG Chatbot 🪐")
    st.caption("Akbank GenAI Bootcamp Projesi. Cevaplar sadece 'sistem.pdf'ten alınmıştır. 🛰️")
    st.write("🌍 Bu chatbot, gezegenler ve yerkürenin yapısı hakkında sorularınızı yanıtlar.")


    # API Anahtarını al ve kontrol et (os.environ'dan kontrol eder)
    if "GEMINI_API_KEY" not in os.environ:
        st.error("Lütfen Gemini API Anahtarınızı giriniz. Anahtar olmadan sistem çalışmaz.")
        key = st.text_input("API Anahtarı:", type="password")
        if key:
            os.environ["GEMINI_API_KEY"] = key
            st.session_state["api_set"] = True
            st.rerun()
        return
    
    # RAG Zincirini Yükle
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
                    st.error(f"API hatası oluştu. Lütfen anahtarınızı kontrol edin: {e}")

if __name__ == "__main__":
    main()
