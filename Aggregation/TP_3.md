# Exercice MongoDB : Manipulation et Agrégation de Données de Commandes

Cet exercice vous guidera à travers le processus d'insertion de données de commandes dans MongoDB, la réalisation d'agrégations pour analyser ces données, puis l'utilisation de jointures pour intégrer des informations depuis une collection de clients. Vous travaillerez avec deux collections : `commandes` pour les détails des commandes et `clients` pour les informations sur les clients.

## Objectif

L'objectif est de pratiquer l'insertion de données, les agrégations basiques et avancées, ainsi que les jointures entre collections dans MongoDB.

## Partie 1: Insertion des Données de Commandes

### Instructions

1. Créez une nouvelle collection nommée `commandes`.
2. Insérez les données des commandes fournies dans la collection `commandes`.
```py
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.ventesDB

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
```

## Partie 2: Agrégations Classiques

Effectuez des opérations d'agrégation basiques sur la collection `commandes`.

### Instructions

1. Calculez le montant total des ventes.
2. Trouvez le nombre moyen de produits par commande.
```py
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
```

3. Déterminez le montant maximum d'une commande.
```py
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
```

## Partie 3: Jointure avec la Collection Clients

Réalisez une jointure entre les collections `commandes` et `clients` pour enrichir les données des commandes avec les informations des clients.

### Instructions

1. Utilisez l'opération `$lookup` pour joindre les collections `commandes` et `clients` sur le champ `idClient`.
2. Affichez le nom du client avec le détail de chaque commande.
```py
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
```

## Partie 4: Agrégations Plus Complexes

Après avoir joint les collections, effectuez des agrégations plus complexes pour obtenir des insights approfondis.

### Instructions

1. Calculez le montant total des commandes par client.
```py
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
```

2. Identifiez le produit le plus vendu.
```py
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
```

3. Trouvez le client ayant effectué le plus grand nombre de commandes.
```py
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
```

4. Trouvez le client ayant commandé le plus grand nombre de produits.

```py
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
```

## Conclusion

Cet exercice vous aidera à maîtriser les techniques d'insertion de données, d'agrégation et de jointure dans MongoDB. Il vous fournira également des insights précieux sur la manipulation et l'analyse de données de ventes complexes.