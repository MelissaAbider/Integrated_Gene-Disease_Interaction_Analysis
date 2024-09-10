import uuid
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

CHROMA_PATH="chroma"

def embedding_modele():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    #embeddings = txtai.Embeddings(path="neuml/pubmedbert-base-embeddings", content=True)#specifique au domaine medicale. Le modèle est basé sur BERT et a été spécifiquement pré-entraîné sur un corpus de données provenant de PubMed
    return embeddings


############# faire l'embedding et sauvgarder dans une base de donnée #####################


def embedding(chunks):
    try:
        # Charger ou créer une nouvelle base
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_modele())
        
        # Supprimer tous les documents existants
        print("vider le contenu de la base de donnée")
        db.delete_collection()
        
        print(f"-> Ajout de {len(chunks)} nouveaux documents")
        
        # Générer des IDs uniques pour chaque chunk
        chunk_ids = [str(uuid.uuid4()) for _ in chunks]
        
        # Ajouter tous les chunks à la base de données
        db.add_documents(chunks, ids=chunk_ids)

        print(f"Embedded {len(chunks)} chunks et sauvegardé dans Chroma")
        return db
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        return None


