import requests
import json

'''Récupérer les titres des articles dont provient chaque morceau de texte'''

def extract_titles_articles(med_id):
    # Construire l'URL avec l'identifiant MED
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/article/MED/{med_id}?resultType=lite&format=json"
    
    # Effectuer la requête GET
    response = requests.get(url)
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        try:
            data = response.json()
            # Extraire le titre de l'article
            title = data.get('result', {}).get('title', 'Titre non disponible')
            print(f"Titre récupéré pour l'ID MED {med_id}: {title}")  
            return title
        except ValueError as e:
            print(f"Erreur lors du décodage JSON pour l'ID MED {med_id}: {e}")
            return None
    else:
        print(f"Erreur HTTP {response.status_code} pour l'ID MED {med_id}: {response.text}")
        return None


'''Récupérer les morcaux d'articles parlant du gene et de la maladie à partir de opentargets'''

def extract_informations(maladie_id, gene_id, fichier_json):
    # URL de l'API GraphQL
    url = "https://api.platform.opentargets.org/api/v4/graphql"

    # Définir la requête GraphQL
    query = """
    query EuropePMCQuery($ensemblId: String!, $efoId: String!, $size: Int!, $cursor: String) {
      disease(efoId: $efoId) {
        id
        europePmc: evidences(
          ensemblIds: [$ensemblId]
          enableIndirect: true
          size: $size
          datasourceIds: ["europepmc"]
          cursor: $cursor
        ) {
          count
          cursor
          rows {
            disease {
              name
              id
            }
            target {
              approvedSymbol
              id
            }
            literature
            textMiningSentences {
              tStart
              tEnd
              dStart
              dEnd
              section
              text
            }
            resourceScore
          }
        }
      }
    }
    """

    # Variables initiales
    size = 50  # Taille de la page, ajustez selon les limites de l'API
    cursor = None
    articles = []

    while True:
        # Définir les variables pour la requête
        variables = {
            "ensemblId": gene_id,
            "efoId": maladie_id,
            "size": size,
            "cursor": cursor
        }

        # Effectuer la requête
        response = requests.post(url, json={'query': query, 'variables': variables})

        print("Réponse de la requête GraphQL reçue.")

        # Vérifier si la requête a réussi
        if response.status_code == 200:
            data = response.json()
            # Extraire les morceaux d'articles
            europe_pmc = data['data']['disease']['europePmc']
            for row in europe_pmc['rows']:
                literature_ids = row['literature']
                for literature_id in literature_ids:
                    titre_article = extract_titles_articles(literature_id)
                    for sentence in row['textMiningSentences']:
                        articles.append({
                            'title': titre_article,
                            'text': sentence['text'],
                            'literature_id': literature_id  # Ajout de l'ID de littérature ( cest un plus )
                        })

            # Vérifier s'il y a une page suivante
            cursor = europe_pmc['cursor']
            if not cursor:
                print("Aucune autre page à récupérer. Fin de la pagination.")
                break
        else:
            print(f"Erreur {response.status_code}: {response.text}")
            break

    # Enregistrer les résultats dans un fichier JSON
    with open(fichier_json, 'w') as f:
        json.dump(articles, f, indent=4)

    print(f"Les données ont été enregistrées dans {fichier_json}.")
