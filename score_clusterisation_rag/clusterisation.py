import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.cluster import KMeans
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance
from bertopic.representation import TextGeneration

def clusterisation(data_path,output):
    
   ''' Fonction pour traiter les données textuelles et effectuer le clustering.'''
   
    device = 'cpu'

    # Charger le dataset
    with open(data_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)

    textes = [doc["text"] for doc in dataset]
    titles = [doc["title"] for doc in dataset]

    # Afficher la longueur des textes et des titres
    print("Length of textes: ", len(textes))
    print("Length of titles: ", len(titles))

    # Modèle LLM
    model_id = "pansophic/rocket-3B"

    # Initialiser le modèle
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map=device)
    model.eval()

    # Calculer les embeddings
    embedding_model = SentenceTransformer("BAAI/bge-small-en")
    embeddings = embedding_model.encode(textes, show_progress_bar=True)

    # Initialiser les modèles de clustering
    umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42)
    kmeans_model = KMeans(n_clusters=10, random_state=0)

    reduced_embeddings = umap_model.fit_transform(embeddings)
    generator = pipeline(
        model=model, tokenizer=tokenizer,
        task='text-generation',
        temperature=0.1,
        max_new_tokens=500,
        repetition_penalty=1.1
    )

    # Prompt engineering
    system_prompt = """
    <s>[INST] <<SYS>>
    You are a helpful, respectful and honest assistant for labeling topics.
    <</SYS>>
    """

    example_prompt = """
    I have a topic that contains the following documents:
    - Signaling Pathway Alterations Driven by BRCA1 and BRCA2 Germline Mutations are Sufficient to Initiate Breast Tumorigenesis by the PIK3CA Oncogene: Single-cell transcriptomics studies have begun to identify breast epithelial cell and stromal cell specific transcriptome differences between BRCA1/2 mutation carriers and non-carriers.
    - Unveiling the relationship between WWOX and BRCA1 in mammary tumorigenicity and in DNA repair pathway selection: Breast cancer is the leading cause of cancer-related deaths in women worldwide, with the basal-like or triple-negative breast cancer (TNBC) subtype being particularly aggressive and challenging to treat.
    - Combination of Resveratrol and PARP inhibitor Olaparib efficiently deregulates homologous recombination repair pathway in breast cancer cells through inhibition of TIP60-mediated chromatin relaxation: This study reveals that RES + OLA treatment inhibited PARP1 activity in the chromatin, and blocked TIP60-mediated chromatin relaxation.

    The topic is described by the following keywords: 'breast cancer, BRCA1, BRCA2, tumorigenesis, DNA repair, signaling pathways, triple-negative breast cancer, treatment, apoptosis'.

    Based on the information about the topic above, please create a short label of this topic. Make sure you to only return the label and nothing more.

    [/INST] Breast Cancer Mechanisms and Treatments
    """
    main_prompt = """
    [INST]
    I have a topic that contains the following documents:
    [DOCUMENTS]

    The topic is described by the following keywords: '[KEYWORDS]'.

    Based on the information about the topic above, please create a short label of this topic. Make sure you to only return the label and nothing more.
    [/INST]
    """
    prompt = system_prompt + example_prompt + main_prompt

    keybert = KeyBERTInspired()
    mmr = MaximalMarginalRelevance(diversity=0.3)
    llama2 = TextGeneration(generator, prompt=prompt)

    representation_model = {"KeyBERT": keybert, "Llama2": llama2, "MMR": mmr}
    vectorizer_model = CountVectorizer(stop_words="english")

    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=kmeans_model,
        representation_model=representation_model,
        vectorizer_model=vectorizer_model,
        top_n_words=10,
        verbose=True
    )
    topics, probs = topic_model.fit_transform(textes, embeddings)
    clusters = topics

    # Afficher les clusters
    print("Clusters pour chaque document :", clusters)

    # Enregistrer les clusters dans un fichier CSV
    clusters_df = pd.DataFrame({'Title': titles, 'Text': textes, 'Cluster': clusters})
    clusters_df.to_csv(output, index=False)
    print("Clusters et textes enregistrés dans 'clusters_with_texts.csv'")

    return clusters

