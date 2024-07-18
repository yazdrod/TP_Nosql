from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.VentesDB

# Création de la collection commandes
commandes_collection = db.commandes

# Insertion des données de commandes
commandes_data = [
    {
        "idCommande": "C001",
        "idClient": 1,
        "montant": 150,
        "produits": [
            {"nom": "Produit 1", "quantite": 1, "prix": 50},
            {"nom": "Produit 2", "quantite": 2, "prix": 50}
        ]
    },
    {
        "idCommande": "C002",
        "idClient": 1,
        "montant": 90,
        "produits": [
            {"nom": "Produit 3", "quantite": 1, "prix": 90}
        ]
    }
]

commandes_collection.insert_many(commandes_data)

total_ventes = commandes_collection.aggregate([
    {
        '$group': {
            '_id': None,
            'totalVentes': {'$sum': '$montant'}
        }
    }
])

print("Montant total des ventes:")
for result in total_ventes:
    print(result)

montant_max_commande = commandes_collection.aggregate([
    {
        '$group': {
            '_id': None,
            'maxMontant': {'$max': '$montant'}
        }
    }
])

print("\nMontant maximum d'une commande:")
for result in montant_max_commande:
    print(result)

clients_collection = db.clients

jointure_commandes_clients = commandes_collection.aggregate([
    {
        '$lookup': {
            'from': 'clients',
            'localField': 'idClient',
            'foreignField': '_id',
            'as': 'clientInfo'
        }
    },
    {
        '$unwind': '$clientInfo'
    },
    {
        '$project': {
            '_id': 0,
            'idCommande': 1,
            'montant': 1,
            'produits': 1,
            'nomClient': '$clientInfo.nom'
        }
    }
])

print("\nDétail des commandes avec le nom du client:")
for result in jointure_commandes_clients:
    print(result)

montant_total_par_client = commandes_collection.aggregate([
    {
        '$group': {
            '_id': '$idClient',
            'totalMontant': {'$sum': '$montant'}
        }
    },
    {
        '$lookup': {
            'from': 'clients',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'clientInfo'
        }
    },
    {
        '$unwind': '$clientInfo'
    },
    {
        '$project': {
            '_id': 0,
            'nomClient': '$clientInfo.nom',
            'totalMontant': 1
        }
    }
])

print("\nMontant total des commandes par client:")
for result in montant_total_par_client:
    print(result)

produit_le_plus_vendu = commandes_collection.aggregate([
    {
        '$unwind': '$produits'
    },
    {
        '$group': {
            '_id': '$produits.nom',
            'totalQuantite': {'$sum': '$produits.quantite'}
        }
    },
    {
        '$sort': {'totalQuantite': -1}
    },
    {
        '$limit': 1
    }
])

print("\nProduit le plus vendu:")
for result in produit_le_plus_vendu:
    print(result)

client_plus_grand_nombre_commandes = commandes_collection.aggregate([
    {
        '$group': {
            '_id': '$idClient',
            'nombreCommandes': {'$sum': 1}
        }
    },
    {
        '$sort': {'nombreCommandes': -1}
    },
    {
        '$limit': 1
    },
    {
        '$lookup': {
            'from': 'clients',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'clientInfo'
        }
    },
    {
        '$unwind': '$clientInfo'
    },
    {
        '$project': {
            '_id': 0,
            'nomClient': '$clientInfo.nom',
            'nombreCommandes': 1
        }
    }
])

print("\nClient ayant effectué le plus grand nombre de commandes:")
for result in client_plus_grand_nombre_commandes:
    print(result)

client_plus_grand_nombre_produits = commandes_collection.aggregate([
    {
        '$unwind': '$produits'
    },
    {
        '$group': {
            '_id': '$idClient',
            'totalProduits': {'$sum': '$produits.quantite'}
        }
    },
    {
        '$sort': {'totalProduits': -1}
    },
    {
        '$limit': 1
    },
    {
        '$lookup': {
            'from': 'clients',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'clientInfo'
        }
    },
    {
        '$unwind': '$clientInfo'
    },
    {
        '$project': {
            '_id': 0,
            'nomClient': '$clientInfo.nom',
            'totalProduits': 1
        }
    }
])

print("\nClient ayant commandé le plus grand nombre de produits:")
for result in client_plus_grand_nombre_produits:
    print(result)