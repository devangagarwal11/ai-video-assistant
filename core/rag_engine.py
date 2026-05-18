import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
from core.vector_store import build_vector_store,load_vector_store,get_retriever

def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3,
    )

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

def build_rag_chain(transcript:str):
    vector_store=build_vector_store(transcript)
    retriever=get_retriever(vector_store,k=4)
    llm=get_llm()

    prompt = ChatPromptTemplate.from_messages(

        [(
            "system",
            """You are an expert meeting assistant. Answer the user's question 
based ONLY on the meeting transcript context provided below.

If the answer is not found in the context, say: 
"I could not find this information in the meeting transcript."

Always be concise and precise. If quoting someone, mention it clearly.

Context from meeting transcript:
{context}""",
        ),
        ("human", "{question}"),
    ]
    )

    ##LCEL rag pipeline
    rag_chain=(
        {"context": retriever | RunnableLambda(format_docs),
         "question":RunnablePassthrough()} | prompt | llm | StrOutputParser()
    )

    return rag_chain

def load_rag_chain():
    vector_store = load_vector_store()
    retriver = get_retriever()

    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an expert meeting assistant. Answer the user's question 
based ONLY on the meeting transcript context provided below.

If the answer is not found in the context, say: 
"I could not find this information in the meeting transcript."

Always be concise and precise. If quoting someone, mention it clearly.

Context from meeting transcript:
{context}""",
        ),
        ("human", "{question}"),
    ])

    rag_chain = (
        {
            "context":  retriver| RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

def ask_question(rag_chain, question:str) -> str:
    print(f"Question : {question}")
    answer = rag_chain.invoke(question)
    print(f"answer :{answer}")
    return answer

# Both functions create the same RAG chain logic, but the main difference is:

# One builds a new vector DB

# vs

# One loads an existing vector DB

# 1. build_rag_chain(transcript)
# Purpose

# Used when:

# You have a new transcript

# and want to:

# split text into chunks
# create embeddings
# store vectors in Chroma
# create retriever
# build RAG chain
# Flow
# Transcript
# ↓
# Chunking
# ↓
# Embeddings
# ↓
# Chroma Vector DB
# ↓
# Retriever
# ↓
# RAG Chain
# This line is key
# vector_store = build_vector_store(transcript)

# This means:

# Create vector DB from scratch

# every time.

# 2. load_rag_chain()
# Purpose

# Used when:

# Vector DB already exists

# and you just want to:

# load existing vectors
# create retriever
# use RAG directly

# without rebuilding embeddings again.







# USE THIS INSTEAD:-
# import os

# def get_rag_chain(transcript: str = None):
#     llm = get_llm()

#     # Check if vector DB already exists
#     if os.path.exists(CHROMA_DIR) and os.listdir(CHROMA_DIR):
#         print("Loading existing vector store...")
#         vector_store = load_vector_store()

#     else:
#         print("Building new vector store...")

#         if not transcript:
#             raise ValueError("Transcript is required to build vector store for first time.")

#         vector_store = build_vector_store(transcript)

#     retriever = get_retriever(vector_store, k=4)

#     prompt = ChatPromptTemplate.from_messages([
#         (
#             "system",
#             """You are an expert meeting assistant.
# Answer the user's question based ONLY on the meeting transcript context.

# If the answer is not found, say:
# 'I could not find this information in the meeting transcript.'

# Context:
# {context}"""
#         ),
#         ("human", "{question}")
#     ])

#     rag_chain = (
#         {
#             "context": retriever | RunnableLambda(format_docs),
#             "question": RunnablePassthrough()
#         }
#         | prompt
#         | llm
#         | StrOutputParser()
#     )

#     return rag_chain