from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('localhost', 27017)
db = client.VentesDB

# Collections
clients_collection = db.client
commandes_collection = db.commandes
ingredients_collection = db.ingredients
sauces_collection = db.sauces

def afficher_menu_principal():
    print("\n--- Menu Principal ---")
    print("1. Nouvelle commande")
    print("2. Voir le chiffre d'affaires")
    print("3. Quitter")
    choix = input("Choisissez une option : ")
    return choix

def nouvelle_commande():
    ingredients = list(ingredients_collection.find())
    sauces = list(sauces_collection.find())

    print("\n--- Choisissez vos ingrédients ---")
    for idx, ing in enumerate(ingredients):
        print(f"{idx + 1}. {ing['nom']} - {ing['prix']} EUR")

    choix_ingredients = input("Entrez les numéros des ingrédients séparés par des virgules : ")
    choix_ingredients = [int(x.strip()) - 1 for x in choix_ingredients.split(',')]

    print("\n--- Choisissez votre sauce ---")
    for idx, sauce in enumerate(sauces):
        print(f"{idx + 1}. {sauce['nom']} - {sauce['prix']} EUR")

    choix_sauce = int(input("Entrez le numéro de la sauce : ")) - 1

    # Calcul du prix total
    prix_total = sum(ingredients[idx]['prix'] for idx in choix_ingredients) + sauces[choix_sauce]['prix']

    # Enregistrement de la commande
    nouvelle_commande = {
        'idCommande': f"C{commandes_collection.count_documents({}) + 1:03d}",
        'idClient': None,  # Assignez une valeur appropriée ici
        'montant': prix_total,
        'produits': [
            {'nom': ingredients[idx]['nom'], 'quantite': 1, 'prix': ingredients[idx]['prix']} for idx in choix_ingredients
        ] + [{'nom': sauces[choix_sauce]['nom'], 'quantite': 1, 'prix': sauces[choix_sauce]['prix']}]
    }
    commandes_collection.insert_one(nouvelle_commande)
    print(f"Commande enregistrée avec succès ! Montant total : {prix_total} EUR")

def voir_chiffre_affaires():
    total_revenue = commandes_collection.aggregate([
        {
            "$group": {
                "_id": None,
                "total": {"$sum": "$montant"}
            }
        }
    ])
    total_revenue = list(total_revenue)
    if total_revenue:
        print(f"Chiffre d'affaires total : {total_revenue[0]['total']} EUR")
    else:
        print("Aucune commande enregistrée.")

def quitter_application():
    print("Merci d'avoir utilisé l'application de commande de sandwichs. À bientôt !")
    exit()

def main():
    while True:
        choix = afficher_menu_principal()
        if choix == '1':
            nouvelle_commande()
        elif choix == '2':
            voir_chiffre_affaires()
        elif choix == '3':
            quitter_application()
        else:
            print("Option invalide. Veuillez choisir une option valide.")

if __name__ == "__main__":
    main()
