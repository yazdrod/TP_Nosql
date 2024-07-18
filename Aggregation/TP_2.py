from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.VentesDB
clients_collection = db.clients

# Pipeline d'agrégation pour le total des ventes par client
total_ventes_par_client = clients_collection.aggregate([
    {
        '$unwind': '$commandes'
    },
    {
        '$group': {
            '_id': '$nom',
            'totalVentes': {'$sum': '$commandes.montant'}
        }
    }
])

print("Total des ventes par client:")
for client in total_ventes_par_client:
    print(client)

# Pipeline d'agrégation pour le panier moyen par commande
panier_moyen_par_commande = clients_collection.aggregate([
    {
        '$unwind': '$commandes'
    },
    {
        '$project': {
            'nombreProduits': {'$size': '$commandes.produits'}
        }
    },
    {
        '$group': {
            '_id': None,
            'totalProduits': {'$sum': '$nombreProduits'},
            'totalCommandes': {'$sum': 1}
        }
    },
    {
        '$project': {
            '_id': 0,
            'panierMoyen': {'$divide': ['$totalProduits', '$totalCommandes']}
        }
    }
])

print("\nPanier moyen par commande:")
for result in panier_moyen_par_commande:
    print(result)

# Pipeline d'agrégation pour le panier moyen par commande
panier_moyen_par_commande = clients_collection.aggregate([
    {
        '$unwind': '$commandes'
    },
    {
        '$project': {
            'nombreProduits': {'$size': '$commandes.produits'}
        }
    },
    {
        '$group': {
            '_id': None,
            'totalProduits': {'$sum': '$nombreProduits'},
            'totalCommandes': {'$sum': 1}
        }
    },
    {
        '$project': {
            '_id': 0,
            'panierMoyen': {'$divide': ['$totalProduits', '$totalCommandes']}
        }
    }
])

print("\nPanier moyen par commande:")
for result in panier_moyen_par_commande:
    print(result)

# Pipeline d'agrégation pour la commande la plus élevée par client
commande_maxi_par_client = clients_collection.aggregate([
    {
        '$unwind': '$commandes'
    },
    {
        '$group': {
            '_id': '$nom',
            'commandeMaxi': {'$max': '$commandes.montant'}
        }
    }
])

print("\nCommande maxi par client:")
for client in commande_maxi_par_client:
    print(client)

commandes_collection = db.commandes

# Pipeline d'agrégation pour le top 3 des produits les plus vendus
top_3_produits = commandes_collection.aggregate([
    {
        '$unwind': '$produits'
    },
    {
        '$group': {
            '_id': '$produits.nom',
            'quantiteTotale': {'$sum': '$produits.quantite'}
        }
    },
    {
        '$sort': {'quantiteTotale': -1}
    },
    {
        '$limit': 3
    }
])

print("\nTop 3 des produits les plus vendus:")
for produit in top_3_produits:
    print(produit)

