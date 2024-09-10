
'''fait le chunking grace à un delimitateur'''
def split_text(file_path, delimiter="\n--------\n"):
  
    # Lire le contenu du fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Diviser le texte en utilisant le délimiteur
    chunks = text.split(delimiter)
    
    # Supprimer les espaces vides au début et à la fin de chaque chunk
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    
    return chunks


