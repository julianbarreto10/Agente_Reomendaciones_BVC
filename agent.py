from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader,TextLoader
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import getpass
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from scraping_stocks.stock_history_description import scraping_stocks
from scraping_republic_bank.scraping_republic_bank import scraping_republic_bank
from scraping_news.scraping_news import scraping_news
from scraping_market_analysis.scraping_market_analysis import scraping_market_analysis

import nltk
#nltk.download('punkt_tab')
#nltk.download('averaged_perceptron_tagger_eng')

Fecha="2025-01-01"
stock="ecopetrol"

def agent_bvc(Fecha,stock):
    scraping_stocks(Fecha,stock)
    scraping_republic_bank(Fecha)
    scraping_news(Fecha,stock)
    scraping_market_analysis(Fecha)

    #os.environ["OPENAI_API_KEY"] = getpass.getpass()
    os.environ["OPENAI_API_KEY"] = "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"

    llm = ChatOpenAI(model="gpt-4o-mini")

    loader = DirectoryLoader("agent_utils/docs_rag", glob="**/*.txt",loader_cls=lambda file_path: TextLoader(file_path, encoding="utf-8"))
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(splits, OpenAIEmbeddings())

    # Definir la herramienta de búsqueda
    def search_tool(query: str) -> str:
        """Responde con información sobre acciones colombianas"""
        docs_filtered = vectorstore.similarity_search(query, k=2)
        return " ".join([doc.page_content for doc in docs_filtered])

    # Crear la herramienta de búsqueda
    search = Tool(
        name="search_tool",
        func=search_tool,
        description="Responde con información sobre acciones colombianas")

    tools=[search]

    # Crear memoria compartida entre ambos agentes
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    with open('templates/template_agent_1.txt', 'r') as archivo:
        # Lee el contenido del archivo y lo guarda en una variable str
        template = archivo.read()

    with open('scraping_stocks/info_accion.txt', 'r') as archivo:
        # Lee el contenido del archivo y lo guarda en una variable str
        valor_accion = archivo.read()

    template = template.replace("{valor_accion}", valor_accion).replace("{stock}", stock)

    prompt_agente = PromptTemplate(input_variables=["input", "chat_history", "tools", "tool_names","agent_scratchpad"],
    template=template)

    agent = create_react_agent(llm, tools, prompt_agente)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

  
    with open('templates/template_agent_2.txt', 'r') as archivo:
        # Lee el contenido del archivo y lo guarda en una variable str
        template_2 = archivo.read()

    template_2 = template_2.replace("{stock}", stock)
    history=""
    review_template = PromptTemplate.from_template(template_2)
    input=""
    review_template.format(input=input, chat_history=history)
    chain = review_template | llm

    iterator=5


    # --- Flujo de interacción ---
    for i in range(iterator):  # Puedes ajustar el número de iteraciones según tus necesidades
        # 1. Ejecutar el primer agente para responder sobre una acción
        if i==0:
            response_1=agent_executor.invoke(
                {
                "input": "¿Cuáles son los comportamientos de los precios de la acción de Ecopetrol?",
                # Notice that chat_history is a string, since this prompt is aimed at LLMs, not chat models
                "chat_history": memory.load_memory_variables({})["chat_history"]
                })
            memory.save_context(
                {"input": "¿Cuáles son los comportamientos de los precios de la acción de Ecopetrol?"},
                {"output": response_1["output"]}
                )
            #print("Respuesta del Agente 1:", response_1)
        elif i==(iterator-1):
            response_1 = agent_executor.invoke(
                {
                "input": "Dada la información recopilada dame una sugerencia de inversión entre [compra/vende/mantén] para la acción (Usa las mismas palabras para dar la sugerencia). Básate únicamente en la información que ya recolectaste. y menciona el porqué de la sugerencia",
                # Notice that chat_history is a string, since this prompt is aimed at LLMs, not chat models
                "chat_history": memory
                })
            memory.save_context(
                {"input": "Dada la información recopilada dame una sugerencia de inversión entre [compra/vende/mantén] para la acción (Usa las mismas palabras para dar la sugerencia). Básate únicamente en la información que ya recolectaste. y menciona el porqué de la sugerencia"},
                {"output": response_1["output"]}
                )
            #print("Respuesta del Agente 1:", response_1)
        else:
            input="Qué información adicional debería tener en cuenta, dame por ahora una sola"
            history = "\n".join(f"* {memory.chat_memory.messages[mem-1].content}\n R: {memory.chat_memory.messages[mem].content}" for mem in range(1, len(memory.chat_memory.messages), 2))
            response_2=chain.invoke({"input": input,"chat_history": history,})  
            print("Pregunta generada por Agente 2:", response_2.content)
            response_1=agent_executor.invoke(
                {
                "input": response_2.content,
                # Notice that chat_history is a string, since this prompt is aimed at LLMs, not chat models
                "chat_history": memory
                })
            memory.save_context(
                {"input": response_2.content},
                {"output": response_1["output"]}
                )
            #print("Respuesta del Agente 1:", response_1)
    return response_1["output"]
