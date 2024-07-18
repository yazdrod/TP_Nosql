# Exercice d'Agrégation Avancée avec MongoDB

Cet exercice vous guide à travers une série de tâches d'agrégation en utilisant une collection de données sur des clients et leurs commandes dans une base de données fictive `ventesDB`.

## Contexte

Vous disposez d'une collection `clients` dans MongoDB, contenant des informations sur 5 clients et leurs commandes respectives. Chaque commande comprend un montant et une liste de produits achetés.

## Objectifs

### Tâche 1: Total des Ventes par Client

Calculez le montant total des ventes réalisées par chaque client. Ceci vous permettra de comprendre quel client a contribué le plus au chiffre d'affaires.
```py
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.ventesDB
collection = db.clients

# Pipeline d'agrégation pour le total des ventes par client
total_ventes_par_client = collection.aggregate([
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
```

### Tâche 2: Panier Moyen par Commande

Déterminez le panier moyen en termes de nombre de produits par commande pour l'ensemble des clients. Cette métrique vous aidera à estimer la taille moyenne des commandes passées.

```py
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

```

### Tâche 3: Commande Maxi par Client

Trouvez la commande avec le montant le plus élevé pour chaque client. Cela mettra en évidence les clients qui ont effectué au moins une grosse commande.
```py
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

```

### Tâche 4: Répartition de l’Utilisation des Produits

Identifiez le top 3 des produits les plus vendus en termes de quantité sur l'ensemble des commandes. Cette analyse vous aidera à comprendre les préférences des clients et les produits les plus populaires.
```py
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

```

## Instructions

Pour chaque tâche, construisez un pipeline d'agrégation qui permettra d'extraire les informations demandées. Utilisez des opérations telles que `$group`, `$sum`, `$avg`, `$sort`, et `$project` pour manipuler et analyser les données.

## Résultats Attendus

- **Tâche 1:** Une liste des clients avec leur montant total des achats.
- **Tâche 2:** Le panier moyen en termes de nombre de produits par commande.
- **Tâche 3:** La commande la plus élevée par client.
- **Tâche 4:** Le top 3 des produits les plus vendus.

Ce travail d'agrégation vous fournira une expérience pratique des capacités puissantes de MongoDB pour analyser et résumer des données complexes. Bonne chance!