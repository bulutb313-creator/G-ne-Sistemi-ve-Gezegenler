import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import MultiQueryRetriever
import pdfplumber 

# --- RAG ZİNCİRİNİ BAŞLATAN FONKSİYON ---
@st.cache_resource
def get_rag_chain():
    PDF_DOSYA_ADI = "sistem.pdf"
    file_path = PDF_DOSYA_ADI

    if not os.path.exists(file_path):
        st.error(f"KRİTİK HATA: '{file_path}' dosyası bulunamadı. Lütfen dosyanın GitHub deponuzda yüklü olduğundan emin olun.")
        return None
    try:
        # 1. Veri İşleme
        full_text = "";
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages: full_text += page.extract_text() + "\n\n"
        documents = [Document(page_content=full_text, metadata={"source": file_path})]
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, overlap=200, separators=["\n\n", "\n", " ", ""],)
        texts = text_splitter.split_documents(documents)

        # 2. Vektör Veritabanı Oluşturma
        embedding_model = GoogleGenerativeAIEmbeddings(model="text-embedding-004")
        vectorstore = Chroma.from_documents(documents=texts, embedding=embedding_model)

        # 3. RAG Zinciri Kurulumu
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
        base_retriever = vectorstore.as_retriever(search_kwargs={"k": 8})
        retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)

        # PROMPT ŞABLONU (Analitik ve Zeki)
        prompt_template = """Sen bir GÜNEŞ SİSTEMİ VE JEOFIZIK UZMANISIN. Görevin, sana verilen BAĞLAM'daki bilgileri ANALİZ EDEREK bir cevap SENTEZLEMEKTİR.
        Cevap verirken şunları yap: Bağlamdaki bilgileri dikkatlice oku, bilgiler arasında neden-sonuç ilişkisi kur ve analitik özetler sun. TÜM İLGİLİ DETAYLARI maddeler halinde veya akıcı paragraflarla aktar.

        Eğer cevap KESİNLİKLE BAĞLAM'da yoksa, sadece "Bu konuda elimde yeterli bilgi yok." de.
        BAĞLAM: {context}
        Soru: {question}
        Cevap:"""
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

        qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, chain_type_kwargs={"prompt": PROMPT})
        return qa_chain

    except Exception as e:
        st.error(f"RAG Zinciri Kurulamadı: {e}")
        return None

# --- STREAMLIT ARAYÜZÜ ANA FONKSİYONU ---
def main():
    st.title("🚀 GÜNEŞ SİSTEMİ VE GEZEGENLER RAG Chatbot (Analitik Uzman) 🪐")
    st.caption("Cevaplar 'sistem.pdf' dosyasındaki TÜM bilgilerden analitik sentezlenmiştir. 🛰️")

    # API Anahtarını al ve kontrol et (Ekrandaki hatayı çözen kod)
    if "GEMINI_API_KEY" not in os.environ:
        st.error("Lütfen Gemini API Anahtarınızı giriniz. Anahtar olmadan sistem çalışmaz.")
        key = st.text_input("Gemini API Anahtarı:", type="password") # Etiket: Gemini
        if key:
            os.environ["GEMINI_API_KEY"] = key
            st.rerun()
        return

    # ... (Geri kalan sohbet mantığı)

if __name__ == "__main__":
    main()
