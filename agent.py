from langchain_community.document_loaders import DirectoryLoader
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
import getpass
import os
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = getpass.getpass()


llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

loader = DirectoryLoader("agent_utils/docs_rag", glob="**/*.txt")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()

with open('template.txt', 'r') as archivo:
    # Lee el contenido del archivo y lo guarda en una variable str
    review_template_str = archivo.read()


review_template = PromptTemplate.from_template(review_template_str)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

template = review_template


custom_rag_prompt = PromptTemplate.from_template(template)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)

rag_chain.invoke("Ten presente el analisis de mercado y las minutas del banco de la republica que se te dieron")
