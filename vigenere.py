# vigenere.py
def vigenere_chiffrer(message, cle):
    """
    Chiffre un message avec l'algorithme de Vigénère.
    
    """
    #Chaque lettre du message est décalée selon la lettre correspondante de la clé (répétée). Les caractères non alphabétiques (espaces, ponctuation) sont conservés tels quels.

    resultat = ""                              # Chaîne qui va contenir le message chiffré final
    cle_index = 0                              # Indice dans la clé (on avance seulement sur les lettres)
    cle_longueur = len(cle)                    # Longueur de la clé (pour faire % plus tard)

    for char in message:                       # On parcourt chaque caractère du message
        if 'a' <= char <= 'z':                 # Si c'est une lettre minuscule
            # On prend la lettre courante de la clé (répétée avec % cle_longueur)
            # .lower() pour être sûr d'avoir une minuscule
            decalage = ord(cle[cle_index % cle_longueur].lower()) - ord('a')
            # On applique le décalage de César avec cette lettre de clé
            # ord(char) - ord('a') → position 0-25
            # + decalage → on décale
            # % 26 → on boucle dans l'alphabet
            # + ord('a') → on revient à la lettre
            resultat += chr(((ord(char) - ord('a') + decalage) % 26) + ord('a'))
            cle_index += 1                     # On avance dans la clé (seulement pour les lettres !)

        elif 'A' <= char <= 'Z':               # Si c'est une lettre majuscule
            # Même principe mais avec les majuscules
            decalage = ord(cle[cle_index % cle_longueur].upper()) - ord('A')
            resultat += chr(((ord(char) - ord('A') + decalage) % 26) + ord('A'))
            cle_index += 1                     # On avance dans la clé

        else:
            # Si c'est un espace, un chiffre, un "!", un "-", etc. → on ne touche pas
            # Et surtout : on N'AVANCE PAS dans la clé !
            resultat += char

    return resultat                            # On retourne le message chiffré complet


def vigenere_dechiffrer(message, cle):
    """
    Déchiffre un message chiffré avec l'algorithme de Vigénère.
    
    """
    #On fait exactement l'inverse : on soustrait le décalage au lieu de l'ajouter.

    resultat = ""                              # Chaîne qui contiendra le message déchiffré
    cle_index = 0                              # Indice courant dans la clé
    cle_longueur = len(cle)                    # Longueur de la clé (utile pour le modulo)

    for char in message:                       # On parcourt chaque caractère du message chiffré
        if 'a' <= char <= 'z':                 # Lettre minuscule chiffrée
            decalage = ord(cle[cle_index % cle_longueur].lower()) - ord('a')
            # Pour déchiffrer : on SOUSTRAIT le décalage au lieu d'ajouter
            # +26 pour éviter les nombres négatifs avant le modulo
            resultat += chr(((ord(char) - ord('a') - decalage + 26) % 26) + ord('a'))
            cle_index += 1                     # On avance dans la clé

        elif 'A' <= char <= 'Z':               # Lettre majuscule chiffrée
            decalage = ord(cle[cle_index % cle_longueur].upper()) - ord('A')
            resultat += chr(((ord(char) - ord('A') - decalage + 26) % 26) + ord('A'))
            cle_index += 1

        else:
            # Caractères non alphabétiques → on les recopie tels quels
            # Et on ne touche PAS à cle_index
            resultat += char

    return resultat                            # Message clair retrouvé




#****************** Tester *********************#

# Ce bloc s'exécute uniquement si on lance ce fichier directement (ex: python vigenere.py)
if __name__ == "__main__":
    # === Test autonome du module Vigénère ===
    texte_clair = "Attack at dawn"             # Message original (avec espaces)
    cle_vigenere = "LEMON"                     # Clé classique de l'exemple célèbre

    # On chiffre le message
    texte_chiffre_vigenere = vigenere_chiffrer(texte_clair, cle_vigenere)

    # Affichage des résultats
    print(f"Texte clair (Vigénère): {texte_clair}")
    print(f"Clé (Vigénère): {cle_vigenere}")
    print(f"Texte chiffré (Vigénère): {texte_chiffre_vigenere}")

    # On déchiffre pour vérifier que ça marche dans les deux sens
    texte_dechiffre_vigenere = vigenere_dechiffrer(texte_chiffre_vigenere, cle_vigenere)
    print(f"Texte déchiffré (Vigénère): {texte_dechiffre_vigenere}")

    # Si tout est bon → on retrouve exactement "Attack at dawn"