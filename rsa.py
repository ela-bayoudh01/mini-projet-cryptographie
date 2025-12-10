# rsa.py
# Module implémentant un RSA  fait main (sans bibliothèque externe)

import math                   
import random                  # Pour choisir aléatoirement la clé publique e


# ====================== VÉRIFICATION SI UN NOMBRE EST PREMIER ======================
def est_premier(n):
    
    #Teste si un nombre n est premier (algorithme optimisé )
    #Très efficace pour les petits nombres (parfait pour un projet pédagogique)
    
    if n < 2:                                   # 0, 1 et nombres négatifs → pas premiers
        return False
    if n in (2, 3):                             # 2 et 3 sont premiers
        return True
    if n % 2 == 0 or n % 3 == 0:                # Élimine tous les multiples de 2 et 3
        return False
    i = 5                                       # On commence à tester à partir de 5
    while i * i <= n:                           # On teste jusqu'à la racine carrée de n
        if n % i == 0 or n % (i + 2) == 0:       # On teste i et i+2 (ex: 5,7 puis 11,13...)
            return False                        # Si divisible → pas premier
        i += 6                                  # On passe au prochain couple (6k±1)
    return True                                 # Si aucun diviseur trouvé → c'est premier !


# ====================== PGCD (Plus Grand Commun Diviseur) - Algorithme d'Euclide ======================
def pgcd(a, b):
    
    #Calcule le PGCD de a et b avec l'algorithme d'Euclide (très rapide)
    #On en a besoin pour vérifier que e et φ(n) sont premiers entre eux
    
    while b:                                    # Tant que b != 0
        a, b = b, a % b                         # On remplace a par b, et b par le reste
    return a                                    # Quand b = 0 → a est le PGCD


# ====================== CHOIX DE e (clé publique) ======================
def generer_e(phi_n):
   
    # Choisit un nombre e aléatoire tel que : 1 < e < φ(n) ,  pgcd(e, φ(n)) = 1 → e et φ(n) sont premiers entre eux (condition OBLIGATOIRE en RSA)
    
    e = random.randrange(2, phi_n)              # On tire un nombre aléatoire entre 2 et φ(n)-1
    while pgcd(e, phi_n) != 1:                  # Tant que e n'est pas premier avec φ(n)
        e = random.randrange(2, phi_n)          # On en tire un nouveau
    return e                                    # On retourne un bon e


# ====================== INVERSE MODULAIRE (trouver d tel que e × d ≡ 1 (mod φ(n))) ======================
def mod_inverse(a, m):
    
    # Calcule l'inverse modulaire de a modulo m avec l'algorithme d'Euclide étendu
    # C'est-à-dire : trouve d tel que (a × d) % m = 1
    # Indispensable pour avoir la clé privée d
    
    m0, x0, x1 = m, 0, 1                        # On sauvegarde m et on initialise les variables
    if m == 1:                                  # Cas particulier (rare)
        return 0
    while a > 1:                                # Tant que a n'est pas réduit à 1
        q = a // m                              # Quotient de la division euclidienne
        m, a = a % m, m                         # On met à jour m et a
        x0, x1 = x1 - q * x0, x0                # Mise à jour des coefficients
    return x1 + m0 if x1 < 0 else x1            # On rend d positif


# ====================== GÉNÉRATION COMPLÈTE DES CLÉS RSA ======================
def rsa_generer_cles():
    print("\n=== Génération des clés RSA (version pédagogique) ===")
    
    # --- Saisie et vérification de p ---
    while True:                                 # Boucle jusqu'à avoir un bon p
        try:
            p = int(input("Entrez un nombre premier p (ex: 61, 101, 53) : "))
            if est_premier(p) and p > 10:       # On accepte seulement les premiers > 10
                print(f"p = {p} est premier")
                break
            else:
                print("Erreur : ce nombre n'est pas premier ou trop petit.")
        except ValueError:                      # Si l'utilisateur tape du texte
            print("Entrez un nombre entier valide.")

    # --- Saisie et vérification de q ---
    while True:
        try:
            q = int(input("Entrez un autre nombre premier q ≠ p (ex: 53, 97) : "))
            if q == p:                          # p et q doivent être différents
                print("q doit être différent de p !")
                continue
            if est_premier(q) and q > 10:
                print(f"q = {q} est premier")
                break
            else:
                print("Erreur : ce nombre n'est pas premier.")
        except ValueError:
            print("Entrez un nombre entier valide.")

    # --- Calculs mathématiques de base du RSA ---
    n = p * q                                   # Module commun aux deux clés
    phi_n = (p - 1) * (q - 1)                   # Fonction d'Euler φ(n)
    e = generer_e(phi_n)                        # Clé publique (choisie aléatoirement)
    d = mod_inverse(e, phi_n)                   # Clé privée (calculée)

    # --- Affichage clair des résultats ---
    print(f"\nClés générées avec succès !")
    print(f"n  = p × q       = {n}")
    print(f"φ(n)             = {phi_n}")
    print(f"Clé publique  (e, n)  = ({e}, {n})")
    print(f"Clé privée    (d, n)  = ({d}, {n})")

    # On retourne seulement les deux clés nécessaires pour chiffrer/déchiffrer
    return (e, n), (d, n)


# ====================== CHIFFREMENT PAR BLOCS (pour messages longs) ======================
def rsa_chiffrer(message, cle_publique):
    e, n = cle_publique                         # On récupère e et n de la clé publique
    if isinstance(message, str):                # Si c'est du texte
        message_bytes = message.encode('utf-8') # On le convertit en bytes
    else:
        message_bytes = message                 # Sinon c'est déjà des bytes

    # On calcule la taille maximale d'un bloc (en bytes) que n peut contenir
    bloc_size = (n.bit_length() - 1) // 8       # -1 pour éviter les dépassements

    blocs_chiffres = []                         # Liste qui contiendra tous les blocs chiffrés
    for i in range(0, len(message_bytes), bloc_size):  # On découpe en blocs
        bloc = message_bytes[i:i + bloc_size]   # On prend un morceau du message
        m = int.from_bytes(bloc, 'big')         # On convertit ce morceau en grand nombre
        c = pow(m, e, n)                        # CHIFFREMENT : c = m^e mod n (magie de Python !)
        blocs_chiffres.append(c)                # On stocke le bloc chiffré

    return blocs_chiffres                       # On retourne la liste complète


# ====================== DÉCHIFFREMENT ======================
def rsa_dechiffrer(blocs_chiffres, cle_privee):
    d, n = cle_privee                           # On récupère d et n de la clé privée
    message_bytes = b""                         # Chaîne binaire qui va reconstruire le message

    for c in blocs_chiffres:                    # Pour chaque bloc chiffré
        m = pow(c, d, n)                        # DÉCHIFFREMENT : m = c^d mod n
        byte_len = (m.bit_length() + 7) // 8    # On calcule combien de bytes il faut
        bloc_bytes = m.to_bytes(byte_len, 'big')  # On reconvertit le nombre en bytes
        message_bytes += bloc_bytes             # On ajoute au message final

    # On reconvertit tout en texte lisible
    return message_bytes.decode('utf-8', errors='ignore').rstrip('\x00')





# *********************** TEST AUTONOME DU MODULE *******************
if __name__ == "__main__":
    # Ce code s'exécute seulement si on lance : python rsa.py
    pub, priv = rsa_generer_cles()              # On génère une paire de clés
    msg = input("\nEntrez n'importe quel message (même très long) : ")
    print("Chiffrement en cours...")
    chiffré = rsa_chiffrer(msg, pub)            # On chiffre → donne une liste
    print(f"Message chiffré en {len(chiffré)} blocs : {chiffré}")

    dechiffré = rsa_dechiffrer(chiffré, priv)   # On déchiffre
    print(f"Message déchiffré : {dechiffré}")
    print("Succès !" if dechiffré == msg else "Échec")