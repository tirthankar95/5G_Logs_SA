from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings 

model_embed_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
hf = HuggingFaceEmbeddings(model_name = model_embed_name, \
                           model_kwargs = model_kwargs, \
                           encode_kwargs = encode_kwargs)
vector_db_dir = "./5Gdbx"
vectorstore = Chroma(embedding_function = hf, persist_directory = vector_db_dir)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
def QA(question):
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    rdocs = retriever.invoke(question)
    fmt_docs = format_docs(rdocs)
    return {"context": fmt_docs, "question": question}
# ========================================================== #
template0 = """You are an AI assistant in the software industry who is 
supposed to answer questions based on 5G logs records provided in the 
context, If you don't know the answer, just say that you don't know, 
don't try to make up an answer.

Context: {context}

Question: {question}

Answer:"""
prompt = PromptTemplate(intput = ["context", "question"], template = template0)
# ========================================================== #
# model_id = "openai-community/gpt2"
model_id = "HuggingFaceH4/zephyr-7b-beta"
# model_id = "microsoft/Phi-3.5-mini-instruct"
llm = HuggingFaceEndpoint(repo_id = model_id, temperature = 0.1)
# ========================================================== #
def StopHallucinations(response):
    return response.split("Question:")[0]
# ========================================================== #
rag_chain = (
    QA
    | prompt
    | llm
    | StrOutputParser()
    | StopHallucinations
)
def ask_me_anything(query, history):
    print(history)
    return rag_chain.invoke(query)
# ========================================================== #