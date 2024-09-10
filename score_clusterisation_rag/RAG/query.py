from langchain.prompts import ChatPromptTemplate 
from langchain_community.chat_models import ChatOllama
from RAG.embedding import embedding_modele
from langchain_community.vectorstores import Chroma

CHROMA_PATH="chroma"

rag_template = """ using the following contexte
{context}
Write the summary of the interaction between the following gene and the disease {question}
"""

def query_rag(query_text):
    embedding_f = embedding_modele()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_f)
    # rechercher dans la base de donnees
    results = db.similarity_search_with_score(query_text, k=5)

    # Vérifiez la structure de chaque résultat et accédez au contenu correctement
    context_text = "\n\n---\n\n".join([doc.page_content if hasattr(doc, 'page_content') else str(doc) for doc, _score in results])

    prompt_template = ChatPromptTemplate.from_template(rag_template)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model_local = ChatOllama(model_name="llama3")
    response = model_local.invoke(prompt)
    
    # Extraire uniquement le contenu de la réponse
    return response.content
