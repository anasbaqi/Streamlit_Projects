import streamlit as st
import pandas as pd
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
# The vectorstore we'll be using
from langchain.vectorstores import FAISS
# The LangChain component we'll use to get the documents
from langchain.chains import RetrievalQA
# The embedding engine that will convert our text to vectors
from langchain.embeddings.openai import OpenAIEmbeddings
#For surfing a csv file instead of manually converting xslx to txt
from langchain.document_loaders import CSVLoader
#For .env keys
from dotenv import load_dotenv
# The easy document loader for text
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
#huggingface Embeddings
from langchain.embeddings import HuggingFaceEmbeddings, HuggingFaceInstructEmbeddings
#HuggingfaceHub for llm
from langchain.llms import HuggingFaceHub
#openai callback to view tokens used
from langchain.callbacks import get_openai_callback as cb
#for monitoring token usage:
import langchain
#for converting pdf to text:
from PyPDF2 import PdfReader



langchain.debug = True


def initiate_llm_HF(input_type):
    #etheir use OpenAI LLM or huggingface LLM:
    llm = HuggingFaceHub(repo_id="google/flan-t5-large", model_kwargs={"temperature": 1, "max_length": 512}, verbose=True)

    # Get your embeddings engine ready
    embeddings = HuggingFaceEmbeddings()

    #free embeddings
    #embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")

    # Embed your documents and combine with the raw text in a pseudo db. Note: This will make an API call to OpenAI
    docsearch = FAISS.from_documents(input_type, embeddings)

    #NOW MAKE RETREIVAL ENGINE
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())
    
    #return the Retreival engine
    return qa


def initiate_llm(input_type):

    # temp = st.slider('How creative would you like the response to be (1 means output is very diverse and creative while 0 means the LLM will not stray from the context)?', 0.0, 1.0, 0.1)
    # st.write('temperate is set to: ', temp)
    
    #etheir use OpenAI LLM or huggingface LLM:
    llm = OpenAI(temperature=1)

    # Get your embeddings engine ready
    embeddings = OpenAIEmbeddings()

    # Embed your documents and combine with the raw text in a pseudo db. Note: This will make an API call to OpenAI
    docsearch = FAISS.from_documents(input_type, embeddings)

    #NOW MAKE RETREIVAL ENGINE
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())
    
    #return the Retreival engine
    return qa
    

def ask_query(qa, question, model_type):
    if model_type == 'OpenAI':
        #prepend question with prompt engineering
        prepend_text = "With the limited data, find an answer to this question and explain how you came to the answer:"
        final_question = prepend_text + "" + question
        
    else:
        final_question = question

    #return the output of the llm with given question
    return qa.run(question)

def pdf_to_text(pdf_doc):
    #raw text file will be stored in this variable
    raw_text = ""
    #create a pdfreader and append to text the text content for each page
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        raw_text += page.extract_text()

    return raw_text

def main():

    load_dotenv()
    #Setting uo streamlit for GUI:
    st.set_page_config(page_title="Bank Data Q&A with ChatGPT :bank: ")
    st.header(" :chart_with_upwards_trend: :blue[Bank Data Q&A with ChatGPT] :chart_with_downwards_trend:")
    st.subheader("A work in progress by Anas AbdulBaqi :construction_worker:")

    #What type of data is the user inserting: 
    option = st.selectbox(
    'What type of file do you want ChatGPT to use? :1234: or :book:',
    ('Choose', 'Excel File', 'Text File', 'PDF File'))

    if option in ('Excel File', 'Text File', 'PDF File'):
        st.write('You selected:', option)
        user_choice = None
        if (option == 'Excel File'):
            user_choice = st.file_uploader("Upload your excel file with bank data", type="xlsx")
        elif(option == 'Text File'):
            user_choice = st.file_uploader("Upload your text file with bank data", type="txt")
        elif(option == 'PDF File'):
            user_choice = st.file_uploader("Upload your text file with bank data", type="pdf")

        #------------------------------------------When a excel file is uploaded------------------------------------------:
        if user_choice is not None:

            #---------------When the file is Excel------------------
            if option == 'Excel File':    
                read_file = pd.read_excel(user_choice)
                #convert to csv:
                csv_file = "bank_analysis.csv"
                read_file.to_csv(csv_file, index= None, header=True)
                df = pd.read_csv(csv_file)
                st.write("your excel sheet: :point_down:")
                st.write(df)
                loader = CSVLoader(file_path="bank_analysis.csv")
                input_type = loader.load()
            #---------------When the file is text---------------------
            elif option == 'Text File':
                 #Load document with their system:
                file_content = user_choice.read()
                # Convert bytes to string (assuming the file contains text)
                text_content = file_content.decode("utf-8")
                text_file = "bank_analysis.txt"
                with open(text_file, "w") as file:
                    file.write(text_content)
                # Initialize the TextLoader with the text content
                loader = TextLoader(text_file)
                doc = loader.load()
                st.write("your text file: :point_down:")
                st.text(text_content)
                #Split the document up:
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators="\n", length_function=len)
                input_type = text_splitter.split_documents(doc)
            #---------------When the file is pdf---------------------
            else:
                #get pdf text:
                raw_text = pdf_to_text(user_choice)
                text_file = "bank_analysis.txt"
                with open(text_file, "w") as file:
                    file.write(raw_text)
                loader = TextLoader(text_file)
                doc = loader.load()
                st.write("your pdf file: :point_down:")
                st.text(raw_text)
                #Split the document up:
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators="\n", length_function=len)
                input_type = text_splitter.split_documents(doc)


            model_type = st.selectbox(
            'What model would you like to use (HuggingFace is free and slow while OpenAI is expensive and fast):',
            ('Choose', 'OpenAI', 'HuggingFace'))
            qa = None
            if model_type in ('OpenAI', 'HuggingFace'):
                st.write('You selected:', model_type)
                if model_type == 'OpenAI':
                    qa = initiate_llm(input_type)
                else:
                    qa = initiate_llm_HF(input_type)
            
            user_question = None
            if qa is not None:
                user_question = st.text_input(" :question: Ask a question about your bank data: ")
            
            #------------When a question is asked--------------
            if user_question is not None and user_question != "": 
                
                #initiate, call, and return th output from the llm: 
                answer = ask_query(qa, user_question, model_type)
                
                #Return user answer:
                st.write(answer)


    
    
if __name__ == "__main__":
    main()