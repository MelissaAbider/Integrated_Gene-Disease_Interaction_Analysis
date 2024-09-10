import requests
from save_json import save_to_json

'''Permet de récupérer les gènes associés à une maladie donnée.
 Il est possible aussi de faire l'inverse et de récupérer les maladies associées à un gène donné. Pour cela, il faut modifier la query'''


def fetch_association_scores(disease_id):
    url = "https://api.platform.opentargets.org/api/v4/graphql" #URL de lal'api de open tragets

    # la requete recuperee : id et nom de la maladie
    #Les cibles associées : leur id, approvedSymbol, et le score d'association
    query = """
    query targetDiseaseAssociations($efoId: String!, $page: Pagination) {
       disease(efoId: $efoId) {
        id 
        name
        associatedTargets(page: $page) {
          count
          rows {
            target {
              id
              approvedSymbol
            }
            score
          }
        }
      }
    }
    """
    
    variables = {
        "efoId": disease_id,
        "page": {
            "size": 50,
            "index": 0
        }
    }

    all_targets = []  # Liste pour stocker tous les gènes associés

# Une requête POST est envoyée à l'API avec la requête et les variables.
    response = requests.post(url, json={"query": query, "variables": variables})
    
    if response.status_code == 200:
        data = response.json()
        
        if 'errors' in data:
            print("Erreur dans la réponse de l'API :", data['errors'])
            return
        
        if data.get("data") is None:
            print("Aucune donnée retournée par l'API.")
            return
        
        
        disease_info = data.get("data", {}).get("disease", {})
        associated_targets = disease_info.get("associatedTargets", {})

        #Le nom de la maladie et le nombre de cibles associées sont affichés.
        print(f"Maladie : {disease_info.get('name')}, Nombre de cibles associées : {associated_targets.get('count')}")
        
        #récupère le nombre total de cibles associées à la maladie à partir de la réponse de l'API
        total_count = associated_targets.get("count", 0)

        #paginer les résultats jusqu'à ce que toutes les cibles soient récupérées
        while len(all_targets) < total_count:
            response = requests.post(url, json={"query": query, "variables": variables})
            
            # convertir la réponse pour pouvoir la traiter 
            if response.status_code == 200:
                data = response.json()
                
                if 'errors' in data:
                    print("Erreur dans la réponse de l'API :", data['errors'])
                    return
                
                if data.get("data") is None:
                    print("Aucune donnée retournée par l'API.")
                    return
                
                associated_targets = data.get("data", {}).get("disease", {}).get("associatedTargets", {})#obtenir les lignes de cibles associées
                rows = associated_targets.get("rows", [])
                
             
                #ajoute les cibles récupérées à la liste all_targets, qui accumule toutes les cibles associées récupérées à travers les différentes pages.
                all_targets.extend(rows)

                #permet de passer à la page suivante lors de la prochaine itération de la boucle
                variables["page"]["index"] += 1
            
            else:
                print(f"Erreur lors de la requête API : {response.status_code} - {response.text}")
                return

    else:
        print(f"Erreur lors de la requête API : {response.status_code} - {response.text}")
        return

    # Suppression si on a des doublons après collecte ( cette partie est importante car j'ai deja eu des doublons)
    unique_targets = {row['target']['id']: row for row in all_targets}.values()

    new_data = {
        "genes": [
            {
                
                "gene_id": row['target']['id'],#l'identifiant unique du gène
                "approved_symbol": row['target']['approvedSymbol'], #approved_symbol
                "scores": [{"score": row['score']}]#score d'association du gène avec la maladie
                #itère sur chaque élément row dans unique_targets.
            } for row in unique_targets
        ]
    }

    save_to_json(new_data)


if __name__ == "__main__":
    disease_id = "MONDO_0007254"  # Identifiant EFO pour le cancer du sein
    fetch_association_scores(disease_id)