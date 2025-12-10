# cesar.py
def cesar_chiffrer(message, cle):
    """
    Chiffre un message en utilisant l'algorithme de César.
    
    """
    resultat = ""                                # Chaîne vide qui va contenir le texte chiffré
    for char in message:                         # On parcourt chaque caractère du message
        if 'a' <= char <= 'z':                   # Si c'est une lettre minuscule
            # On convertit la lettre en position (0 à 25), on ajoute la clé,
            # on fait % 26 pour boucler dans l'alphabet, puis on revient à la lettre
            resultat += chr(((ord(char) - ord('a') + cle) % 26) + ord('a'))
        elif 'A' <= char <= 'Z':                 # Si c'est une lettre majuscule
            # Même principe, mais pour les majuscules
            resultat += chr(((ord(char) - ord('A') + cle) % 26) + ord('A'))
        else:
            # Si c'est un espace, un chiffre, un signe de ponctuation → on le laisse intact
            resultat += char
    return resultat                              # On retourne le message final chiffré


def cesar_dechiffrer(message, cle):
    """
    Déchiffre un message chiffré avec l'algorithme de César.
    
    """
    # Exemple : clé 3 → pour revenir en arrière, on décale de -3 (ou +23)
    return cesar_chiffrer(message, -cle)

#****************** Tester *********************#

# Ce bloc ne s'exécute que si on lance directement ce fichier 

if __name__ == "__main__":
    # Exemple d'utilisation du module César 
    texte_clair = "Bonjour le monde"             # Message original en clair
    cle_cesar = 3                                # Clé de chiffrement choisie (décalage de 3)
    
    # On chiffre le message
    texte_chiffre_cesar = cesar_chiffrer(texte_clair, cle_cesar)
    
    # On affiche les résultats pour vérifier que tout fonctionne
    print(f"Texte clair (César): {texte_clair}")
    print(f"Clé (César): {cle_cesar}")
    print(f"Texte chiffré (César): {texte_chiffre_cesar}")
    
    # On déchiffre pour revenir au message original
    texte_dechiffre_cesar = cesar_dechiffrer(texte_chiffre_cesar, cle_cesar)
    print(f"Texte déchiffré (César): {texte_dechiffre_cesar}")
    
    # Si tout est bon, on devrait revoir "Bonjour le monde"