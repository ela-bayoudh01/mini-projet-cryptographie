# main.py
import cesar
import vigenere
from rsa import (
    rsa_generer_cles,
    rsa_chiffrer,
    rsa_dechiffrer
)

def menu():
    print("\n--- Mini Projet Cryptographie ---")
    print("1. Chiffrer / Déchiffrer avec César")
    print("2. Chiffrer / Déchiffrer avec Vigénère")
    print("3. Chiffrer / Déchiffrer avec RSA")
    print("4. Quitter")
    return input("Choisissez une option : ")


def main():
    # Variables globales pour les clés RSA
    cle_publique_rsa = None   # (e, n)
    cle_privee_rsa = None     # (d, n)

    while True:
        choix = menu()

        # ===============================================
        # 1. César
        # ===============================================
        if choix == '1':
            print("\n--- Algorithme de César ---")
            message = input("Entrez le message : ")
            try:
                cle = int(input("Entrez la clé (nombre entier) : "))
            except ValueError:
                print("Clé invalide !")
                continue

            action = input("Voulez-vous (c)hiffrer ou (d)échiffrer ? ").lower()
            if action == 'c':
                resultat = cesar.cesar_chiffrer(message, cle)
                print(f"Message chiffré : {resultat}")
            elif action == 'd':
                resultat = cesar.cesar_dechiffrer(message, cle)
                print(f"Message déchiffré : {resultat}")
            else:
                print("Action non valide.")

        # ===============================================
        # 2. Vigénère
        # ===============================================
        elif choix == '2':
            print("\n--- Algorithme de Vigénère ---")
            message = input("Entrez le message : ")
            cle = input("Entrez la clé (mot) : ").strip()
            if not cle:
                print("La clé ne peut pas être vide !")
                continue

            action = input("Voulez-vous (c)hiffrer ou (d)échiffrer ? ").lower()
            if action == 'c':
                resultat = vigenere.vigenere_chiffrer(message, cle)
                print(f"Message chiffré : {resultat}")
            elif action == 'd':
                resultat = vigenere.vigenere_dechiffrer(message, cle)
                print(f"Message déchiffré : {resultat}")
            else:
                print("Action non valide.")

        # ===============================================
        # 3. RSA PÉDAGOGIQUE (à la main)
        # ===============================================
        elif choix == '3':
            print("\n--- Algorithme RSA  ---")
            print("1. Générer des clés RSA (saisie de p et q)")
            print("2. Chiffrer un message avec RSA")
            print("3. Déchiffrer un message avec RSA")
            rsa_choix = input("Choisissez une option RSA : ")

            if rsa_choix == '1':
                try:
                    # ON REÇOIT SEULEMENT 2 VALEURS → pas 4 !
                      cle_publique_rsa, cle_privee_rsa = rsa_generer_cles()
                      print("Clés RSA générées avec succès !")
                except Exception as e:
                    print(f"Erreur lors de la génération : {e}")

            elif rsa_choix == '2':
                if cle_publique_rsa is None:
                    print("Veuillez d'abord générer les clés RSA (Option 1).")
                else:
                    message = input("Entrez un message court à chiffrer: ")
                    try:
                        chiffre = rsa_chiffrer(message, cle_publique_rsa)
                        print(f"\nMessage chiffré en {len(chiffre)} bloc(s) :")
                        print(chiffre)  # ← affiche la liste proprement
                        print("\nCopiez cette liste entière pour le déchiffrement !")
                    except ValueError as e:
                        print(f"Erreur : {e}")
                    except Exception as e:
                        print(f"Erreur inattendue : {e}")

            elif rsa_choix == '3':
                if cle_privee_rsa is None:
                    print("Veuillez d'abord générer les clés RSA (Option 1).")
                    
                else:
                    print("\nCollez exactement la liste affichée après le chiffrement")
                    entrée = input("→ ")
                    try:
                        # On accepte la liste telle quelle (grâce à eval – OK pour un projet étudiant)
                       blocs = eval(entrée)
                       if not isinstance(blocs, list):
                           raise ValueError("Ce n'est pas une liste")
                       dechiffre = rsa_dechiffrer(blocs, cle_privee_rsa)
                       print(f"\nMessage déchiffré :\n{dechiffre}")
                    
                    except Exception as e:
                        print(f"Erreur de format ! Assurez-vous de copier-coller la liste entière.")
                        print(f"Erreur lors du déchiffrement : {e}")

            else:
                print("Option RSA non valide.")

        # ===============================================
        # 4. Quitter
        # ===============================================
        elif choix == '4':
            print("Merci d'avoir utilisé le programme. Au revoir !")
            break

        else:
            print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    main()