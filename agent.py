from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
import getpass
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

import nltk
#nltk.download('punkt_tab')
#nltk.download('averaged_perceptron_tagger_eng')

os.environ["OPENAI_API_KEY"] = getpass.getpass()

stock='ecopetrol'
llm = ChatOpenAI(model="gpt-4o-mini")

loader = DirectoryLoader("agent_utils/docs_rag", glob="**/*.txt")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = FAISS.from_documents(splits, OpenAIEmbeddings())

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})


with open('templates/template.txt', 'r') as archivo:
    # Lee el contenido del archivo y lo guarda en una variable str
    review_template_str = archivo.read()


url_context = f'templates/{stock}_context/context.txt'

with open(url_context, 'r') as archivo:
    # Lee el contenido del archivo y lo guarda en una variable str
    context = archivo.read()


with open('scraping_stocks/info_accion.txt', 'r') as archivo:
    # Lee el contenido del archivo y lo guarda en una variable str
    valor_accion = archivo.read()

review_template_str = review_template_str.replace("{valor_accion}", valor_accion).replace("{stock}", stock)

custom_rag_prompt = PromptTemplate.from_template(review_template_str)


def format_docs(docs):
    print(len(docs))
    print("\n\n".join(doc.page_content for doc in docs))
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "context_stock": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)

rag_chain.invoke(context)
