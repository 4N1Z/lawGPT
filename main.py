import os
import dotenv
import streamlit as st
from dotenv import load_dotenv

from llama_index import  GPTVectorStoreIndex,SimpleDirectoryReader,LLMPredictor, GPTVectorStoreIndex, PromptHelper, ServiceContext
from langchain import OpenAI

#GLOBALS

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
upload_path = './data'


# Fucntion to save the PDF to directory
def save_uploadedfile(uploadedfile):
     with open(os.path.join("data",uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success("Saved File:{} to directory".format(uploadedfile.name))

def get_names(pdf):
     #adding the names of upload to a list
    check_pdf = []
    for uploaded_file in pdf:
        check_pdf.append(uploaded_file.name)


# def is_folder_empty(folder_path):
    return not any(os.scandir(folder_path))


def get_docs():
     
     pdf_s = st.file_uploader("Upload the sylabbus",accept_multiple_files=True,type=['pdf', 'docx','txt'])
     pdf_s_names = get_names(pdf_s)
    #  st.write(pdf_s_names)
     if st.button("process"):
        
        if pdf_s is not None:
            for eachFile in pdf_s : 
                save_uploadedfile(eachFile)
                st.write("Uploaded Successfully")
                
        else :
            st.write("PDF's not Found")
    #After uploading the docs it goes to chat
     main_chat()


def main_chat() :

    st.text_input("Enter you prompy : ", key = "prompt" , placeholder = "Tell me about  ... ")
    st.write("in chat") 
    st.write("error found : Files are not read ! Need to find out .")
     
    if is_folder_empty(upload_path):
        st.write('not uploded, going with default')
    else :
        bulk_documents = SimpleDirectoryReader('./data').load_data()
        bulk_index = GPTVectorStoreIndex.from_documents(bulk_documents)

    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))
    # define prompt helper
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_output = 256
    # set maximum chunk overlap
    max_chunk_overlap = 20
    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    custom_llm_index = GPTVectorStoreIndex.from_documents(
        bulk_documents, service_context=service_context
    )
    query_engine = bulk_index.as_query_engine()
    response = query_engine.query("What are the laws in Kashmir ?")
    st.write(response)


def main ():

    #Knowledge base with bulk data
    st.set_page_config('LawGPT')
    st.header("Get your answers regarding Law")
    # st.subheader("Upload the docs for reference Optional")

#option to either upload and talk 
#or just do the chat

    if st.button("Upload the docs for reference or you want to search (Optional)") :
        get_docs()
    elif st.button("Go To Chat") :
        main_chat()

    


if __name__ == "__main__" :
    main()
