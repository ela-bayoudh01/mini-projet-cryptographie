# rsa.py
# Module implémentant un chiffrement/déchiffrement RSA sécurisé avec la bibliothèque cryptography
# Version "vraie" RSA (2048 bits, OAEP + SHA256) — utilisé dans le monde réel (HTTPS, PGP, etc.)

# ====================== IMPORTATIONS ======================
from cryptography.hazmat.primitives.asymmetric import rsa, padding
# → rsa        : pour générer les clés RSA
# → padding    : pour utiliser le padding OAEP (sécurité contre attaques)

from cryptography.hazmat.primitives import hashes
# → hashes     : pour utiliser SHA256 (fonction de hachage cryptographique sécurisée)

from cryptography.hazmat.primitives import serialization
# → serialization : (non utilisé ici, mais souvent pour sauvegarder les clés dans un fichier)

from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
# → OAEP et MGF1 : schéma de padding moderne et sécurisé (recommandé par les experts)

from cryptography.hazmat.backends import default_backend
# → default_backend() : utilise le meilleur moteur cryptographique disponible sur la machine (OpenSSL, etc.)


# ====================== GÉNÉRATION DES CLÉS ======================
def rsa_generer_cles():
    """
    Génère une paire de clés RSA 2048 bits (standard de sécurité actuel).
    Retourne : (clé_privée, clé_publique)
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,        # Valeur standard (FIPS 186-4) — très utilisée, sûre et rapide
        key_size=2048,                # Taille de la clé en bits → 2048 = niveau de sécurité bancaire/militaire
        backend=default_backend()     # Utilise le moteur cryptographique du système (OpenSSL)
    )
    # La clé publique est dérivée automatiquement de la clé privée
    public_key = private_key.public_key()
    
    # On retourne les deux clés pour les utiliser plus tard
    return private_key, public_key


# ====================== CHIFFREMENT ======================
def rsa_chiffrer(message, cle_publique):
    """
    Chiffre un message avec la clé publique RSA.
    Seule la clé privée correspondante pourra le déchiffrer.
    Paramètres :
        message      : str ou bytes → texte à chiffrer
        cle_publique : objet clé publique RSA
    Retourne : bytes → message chiffré (format binaire)
    """
    # Si l'utilisateur passe une chaîne texte, on la convertit en bytes (UTF-8 = standard mondial)
    if isinstance(message, str):
        message = message.encode('utf-8')

    # Chiffrement réel avec OAEP + SHA256 (le plus sécurisé aujourd'hui)
    ciphertext = cle_publique.encrypt(
        message,                                      # Données à chiffrer
        padding.OAEP(                                 # Padding moderne et sécurisé
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Masque de génération (MGF1 avec SHA256)
            algorithm=hashes.SHA256(),           # Fonction de hachage utilisée
            label=None                           # Étiquette optionnelle (pas utilisée ici)
        )
    )
    # Retourne le message chiffré sous forme de bytes (impossible à lire directement)
    return ciphertext


# ====================== DÉCHIFFREMENT ======================
def rsa_dechiffrer(texte_chiffre, cle_privee):
    """
    Déchiffre un message chiffré avec la clé privée RSA.
    Paramètres :
        texte_chiffre : bytes → message chiffré (sortie de rsa_chiffrer)
        cle_privee    : objet clé privée RSA
    Retourne : str → message en clair (texte lisible)
    """
    # Déchiffrement avec le même padding OAEP + SHA256 que pour le chiffrement
    plaintext = cle_privee.decrypt(
        texte_chiffre,                                # Message chiffré à déchiffrer
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # On reconvertit les bytes en texte lisible (UTF-8)
    return plaintext.decode('utf-8')


# ====================== TEST AUTONOME ======================
if __name__ == "__main__":
    # Ce code ne s'exécute que si on lance directement ce fichier : python rsa.py
    print("Génération des clés RSA...")                    # Information pour l'utilisateur
    cle_privee_rsa, cle_publique_rsa = rsa_generer_cles()   # On génère une nouvelle paire de clés
    print("Clés RSA 2048 bits générées avec succès.\n")

    # Message à chiffrer
    texte_clair = "Message secret de test pour RSA."
    print(f"Texte clair (RSA) : {texte_clair}")

    # === Chiffrement ===
    print("Chiffrement du message avec RSA...")
    texte_chiffre_rsa = rsa_chiffrer(texte_clair, cle_publique_rsa)
    # On affiche en hexadécimal pour que ce soit lisible (sinon ce serait illisible)
    print(f"Texte chiffré (RSA) : {texte_chiffre_rsa.hex()} (représentation hexadécimale)")

    # === Déchiffrement ===
    print("\nDéchiffrement du message avec RSA...")
    texte_dechiffre_rsa = rsa_dechiffrer(texte_chiffre_rsa, cle_privee_rsa)
    print(f"Texte déchiffré (RSA) : {texte_dechiffre_rsa}")

    # Si tout est bon → on retrouve exactement le message original
    if texte_dechiffre_rsa == texte_clair:
        print("\nSUCCÈS TOTAL : le message a été parfaitement chiffré et déchiffré !")