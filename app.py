import streamlit as st
import os
import pdfplumber 

# --- Hata Giderilmiş ve Güncel Kütüphane Yolları ---
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma 
from langchain_community.retrievers import MultiQueryRetriever
from langchain.chains import RetrievalQA


# --- RAG ZİNCİRİNİ BAŞLATAN FONKSİYON ---
@st.cache_resource
def get_rag_chain():
    """RAG sistemini kurar ve zinciri döndürür. Veri yükleme bu fonksiyon içinde yapılır."""
    PDF_DOSYA_ADI = "sistem.pdf"
    file_path = PDF_DOSYA_ADI

    # 1. DOSYA KONTROLÜ
    if not os.path.exists(file_path):
        st.error(f"KRİTİK HATA: '{file_path}' dosyası GitHub'da bulunamıyor.")
        return None
    try:
        # 2. VERİ İŞLEME (PDF Okuma ve Parçalama)
        full_text = "";
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages: full_text += page.extract_text() + "\n\n"
        documents = [Document(page_content=full_text, metadata={"source": file_path})]
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, overlap=200, separators=["\n\n", "\n", " ", ""],)
        texts = text_splitter.split_documents(documents)

        # 3. Vektör Veritabanı Oluşturma
        embedding_model = GoogleGenerativeAIEmbeddings(model="text-embedding-004")
        vectorstore = Chroma.from_documents(documents=texts, embedding=embedding_model)

        # 4. RAG Zinciri Kurulumu (Analitik Prompt)
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
        base_retriever = vectorstore.as_retriever(search_kwargs={"k": 8})
        retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)

        # ANALİTİK PROMPT ŞABLONU
        prompt_template = """Sen bir GÜNEŞ SİSTEMİ VE JEOFIZIK UZMANISIN. Görevin, sana verilen BAĞLAM'daki bilgileri ANALİZ EDEREK bir cevap SENTEZLEMEKTİR. Neden-sonuç ilişkileri kur, kıyaslamalar yap ve mantıksal çıkarımlar sun.

        Eğer cevap KESİNLİKLE BAĞLAM'da yoksa, sadece "Bu konuda elimde yeterli bilgi yok." diye cevap ver.
        BAĞLAM: {context}
        Soru: {question}
        Cevap:"""
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

        qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, chain_type_kwargs={"prompt": PROMPT})
        return qa_chain

    except Exception as e:
        st.error(f"RAG Zinciri Kurulamadı. Lütfen API Anahtarınızı ve GitHub dosyalarınızı kontrol edin. Hata: {e}")
        return None

# --- STREAMLIT ARAYÜZÜ ANA FONKSİYONU ---
def main():
    st.set_page_config(page_title="Analitik Chatbot", layout="wide")
    st.title("🚀 GÜNEŞ SİSTEMİ VE GEZEGENLER RAG Chatbot (Analitik Uzman) 🪐")
    st.caption("Cevaplar 'sistem.pdf' dosyasındaki TÜM bilgilerden analitik sentezlenmiştir. Streamlit Cloud'da kalıcı yayında. 🛰️")

    # API Anahtarını al ve kontrol et (Secrets'ı okur)
    if "GEMINI_API_KEY" not in os.environ:
        st.error("Lütfen Gemini API Anahtarınızı giriniz. Anahtar olmadan sistem çalışmaz.")
        # Bu kısım sadece Secret'ı girmeyi unuttuğunuzda ekranda çıkar.
        key = st.text_input("Gemini API Anahtarı:", type="password", key="api_input") 
        if key:
            os.environ["GEMINI_API_KEY"] = key
            st.rerun()
        return

    # Chain'i başlat
    if "qa_chain" not in st.session_state:
        st.session_state.qa_chain = get_rag_chain()
        if st.session_state.qa_chain is None: return

    if "messages" not in st.session_state: st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])

    if prompt := st.chat_input("Güneş Sistemi hakkında analitik bir soru sorun..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analiz ediliyor... Neden-sonuç ilişkileri kuruluyor... 🧠"):
                try:
                    answer = st.session_state.qa_chain.run(prompt)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"API hatası oluştu veya zincir çalıştırılamadı. Hata: {e}")

if __name__ == "__main__":
    main()
