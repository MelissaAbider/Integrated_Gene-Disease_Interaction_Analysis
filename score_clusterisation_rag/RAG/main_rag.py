from RAG.chunking import split_text
from RAG.embedding import embedding
from RAG.query import query_rag


def function(prompt, cluster_textes_path) -> str:  
   
    new_chunks = split_text(cluster_textes_path)

    vectorstore = embedding(new_chunks)

    # Utiliser RAG pour interroger la base de données
    print("\n\n ----- Answer with RAG : -----\n")

    result_with_rag = query_rag(prompt)
    return result_with_rag


