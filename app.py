import streamlit as st
import os
from getpass import getpass
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- AYARLAR VE ÇALIŞTIRMA FONKSİYONLARI ---

def load_environment():
    """Gemini API Anahtarını alır veya kontrol eder."""
    # API Anahtarının sistemde ayarlı olup olmadığını kontrol et
    if "GEMINI_API_KEY" not in os.environ:
        # Colab'da anahtarı girmesi istenir (Streamlit arayüzü üzerinden)
        st.error("Lütfen Gemini API Anahtarınızı aşağıdaki alana giriniz.")
        
        # Kullanıcıdan API anahtarını alması için bir kutu göster
        gemini_key = st.text_input("Gemini API Anahtarınızı Yapıştırın:", type="password")
        
        if gemini_key:
            os.environ["GEMINI_API_KEY"] = gemini_key
            os.environ["GOOGLE_API_KEY"] = gemini_key
            st.success("API Anahtarı başarıyla ayarlandı!")
            st.experimental_rerun() # Anahtar ayarlandıktan sonra uygulamayı yeniden başlat
        else:
            return False # Anahtar yoksa ana fonksiyonda devam etme
    return True # Anahtar varsa devam et

@st.cache_resource # Bu fonksiyonun sadece bir kere çalışmasını sağla (hız için önemli)
def get_rag_chain():
    """PDF'i yükler, parçalar, vektör veritabanı oluşturur ve RAG zincirini döndürür."""
    # 1. Dosya Kontrolü
    pdf_dosya_adi = "sistem.pdf"
    if not os.path.exists(pdf_dosya_adi):
        st.error(f"'{pdf_dosya_adi}' dosyası bulunamadı. Lütfen Colab'a yüklediğinizden emin olun.")
        return None

    # 2. Yükleme ve Parçalama (Komut 17)
    loader = PyPDFLoader(pdf_dosya_adi)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=4000,
        chunk_overlap=500,
        length_function=len,
        is_separator_regex=False,
    )
    splits = text_splitter.split_documents(documents)

    # 3. Gömme Modeli ve Retriever (Komut 8 ve 12)
    embedding_model = GoogleGenerativeAIEmbeddings(model="text-embedding-004")
    vector_store = FAISS.from_documents(splits, embedding_model)
    retriever = vector_store.as_retriever(search_kwargs={"k": 6}) # En alakalı 6 parçayı çek

    # 4. LLM ve Prompt (Komut 18 - Sert Prompt)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)
    
    final_answer_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Sen bir Jeofizik ve Uzay Bilimleri chatbotusun. Görevin, sağlanan BAĞLAM'daki (context) bilgileri kullanarak kullanıcının sorularını AKICI, DOĞRU ve DETAYLI olarak cevaplamaktır. Cevabını yalnızca BAĞLAM'da yer alan gerçeklere dayandır.
                
                Eğer BAĞLAM soruyu cevaplamak için yeterli bilgiyi İÇERMİYORSA, durumu nazikçe belirterek 'Üzgünüm, bu bilgiye sağlanan kaynakta yeterince detaylı ulaşılamamaktadır. Lütfen "sistem.pdf" dosyasındaki diğer konuları deneyiniz.' şeklinde cevap ver. Asla uydurma bilgi verme.
                
                BAĞLAM: {context}""",
            ),
            ("human", "{input}"),
        ]
    )
    
    document_chain = create_stuff_documents_chain(llm, final_answer_prompt)
    rag_chain = create_retrieval_chain(retriever, document_chain)
    
    return rag_chain

# --- STREAMLIT ARAYÜZÜ ANA FONKSİYONU ---

def main():
    st.title("Jeofizik ve Güneş Sistemi RAG Chatbot")
    st.caption("Dr. Begüm Çıvgın'ın 'sistem.pdf' dosyasındaki bilgilere dayalı olarak çalışan bir soru-cevap asistanıdır.")
    st.write("Bu chatbot, **yalnızca** sağlanan PDF dosyasını kullanarak cevap üretir.")

    # 1. API Anahtarını Kontrol Et (Anahtar yoksa kullanıcıdan ister)
    if not load_environment():
        return

    # 2. RAG Zincirini Yükle (Hızlı olması için sadece bir kere yüklenir)
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = get_rag_chain()
        if st.session_state.rag_chain is None:
            return
        
    rag_chain = st.session_state.rag_chain

    # 3. Sohbet Geçmişini Başlat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Geçmişteki mesajları göster
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 4. Kullanıcıdan Soru Al
    if prompt := st.chat_input("PDF hakkında bir soru sorabilirsiniz..."):
        
        # Kullanıcı mesajını kaydet ve göster
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Chatbot'tan cevap al
        with st.chat_message("assistant"):
            with st.spinner("Cevap aranıyor..."):
                response = rag_chain.invoke({"input": prompt})
                answer = response["answer"]
                st.markdown(answer)

        # Cevabı geçmişe kaydet
        st.session_state.messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()
