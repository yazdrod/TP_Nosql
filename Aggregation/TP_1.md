# Exercice Avancé sur la Base de Données Pokémon GO

Cet exercice propose une série de tâches pour explorer les fonctionnalités avancées de MongoDB, en utilisant la collection Pokémon GO. Les étapes couvrent l'ajout de données, l'agrégation de statistiques, et l'analyse de documents.

## Étape 1: Ajout de Statistiques Aléatoires

Votre première tâche consiste à enrichir chaque document Pokémon avec des statistiques d'attaque et de défense générées aléatoirement.

### Instructions

- Parcourez chaque document de la collection `pokemonGO`.
- Générez des statistiques aléatoires pour l'attaque et la défense (valeurs entre 1 et 100).
- Mettez à jour chaque Pokémon avec ces nouvelles statistiques sous un objet `stats`.
```py
from pymongo import MongoClient
import random

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.PokemonDB
collection = db.Pokemons

# Parcourir chaque document et ajouter des statistiques aléatoires
for pokemon in collection.find():
    attack = random.randint(1, 100)
    defense = random.randint(1, 100)
    
    collection.update_one(
        {'_id': pokemon['_id']},
        {'$set': {'stats': {'attack': attack, 'defense': defense}}}
    )

```


## Étape 2: Agrégation des Statistiques HP et CP

Effectuez une analyse détaillée des Points de Vie (HP) et des Points de Combat (CP) des Pokémon.

### Instructions

- Calculez la moyenne des HP et des CP pour l'ensemble des Pokémon.
- Calculez la moyenne des HP et des CP par type.
- Déterminez le Pokémon ayant le HP et le CP les plus élevés.
```py
# Moyenne des HP et des CP pour l'ensemble des Pokémon
avg_hp_cp = collection.aggregate([
    {
        '$group': {
            '_id': None,
            'avgHP': {'$avg': '$hp'},
            'avgCP': {'$avg': '$cp'}
        }
    }
])

print("Moyenne des HP et CP pour tous les Pokémon:")
for result in avg_hp_cp:
    print(result)

# Moyenne des HP et des CP par type
avg_hp_cp_by_type = collection.aggregate([
    {
        '$unwind': '$type'
    },
    {
        '$group': {
            '_id': '$type',
            'avgHP': {'$avg': '$hp'},
            'avgCP': {'$avg': '$cp'}
        }
    }
])

print("\nMoyenne des HP et CP par type:")
for result in avg_hp_cp_by_type:
    print(result)

# Pokémon ayant le HP le plus élevé
max_hp_pokemon = collection.find().sort('hp', -1).limit(1)
print("\nPokémon avec le HP le plus élevé:")
for pokemon in max_hp_pokemon:
    print(pokemon)

# Pokémon ayant le CP le plus élevé
max_cp_pokemon = collection.find().sort('cp', -1).limit(1)
print("\nPokémon avec le CP le plus élevé:")
for pokemon in max_cp_pokemon:
    print(pokemon)
```

## Étape 3: Lecture de Données sur les Documents

Exécutez des requêtes pour extraire des informations ciblées de votre collection.

### Instructions

- Identifiez tous les Pokémon avec plus de 50 d'attaques.
- Sélectionnez les Pokémon avec un CP supérieur à la moyenne des CP.
```py
# Pokémon avec plus de 50 d'attaques
strong_attack_pokemons = collection.find({'stats.attack': {'$gt': 50}})
print("\nPokémon avec plus de 50 d'attaques:")
for pokemon in strong_attack_pokemons:
    print(pokemon)

# Calcul de la moyenne des CP
avg_cp_result = collection.aggregate([
    {
        '$group': {
            '_id': None,
            'avgCP': {'$avg': '$cp'}
        }
    }
])
avg_cp = list(avg_cp_result)[0]['avgCP']

# Pokémon avec un CP supérieur à la moyenne des CP
strong_cp_pokemons = collection.find({'cp': {'$gt': avg_cp}})
print("\nPokémon avec un CP supérieur à la moyenne des CP:")
for pokemon in strong_cp_pokemons:
    print(pokemon)
```

## Étape 4: Agrégation des Statistiques par Type

Analysez les statistiques d'attaque et de défense, en les regroupant par type de Pokémon.

### Instructions

- Calculez la moyenne des statistiques d'attaque et de défense pour chaque Pokémon.
- Comparez les statistiques moyennes d'attaque et de défense de chaque Pokémon groupé par type.
```py
# Moyenne des statistiques d'attaque et de défense pour chaque Pokémon
avg_stats_per_pokemon = collection.aggregate([
    {
        '$project': {
            '_id': 0,
            'name': 1,
            'avgStats': {'$avg': ['$stats.attack', '$stats.defense']}
        }
    }
])

print("\nMoyenne des statistiques d'attaque et de défense pour chaque Pokémon:")
for result in avg_stats_per_pokemon:
    print(result)

# Moyenne des statistiques d'attaque et de défense par type
avg_stats_by_type = collection.aggregate([
    {
        '$unwind': '$type'
    },
    {
        '$group': {
            '_id': '$type',
            'avgAttack': {'$avg': '$stats.attack'},
            'avgDefense': {'$avg': '$stats.defense'}
        }
    }
])

print("\nMoyenne des statistiques d'attaque et de défense par type:")
for result in avg_stats_by_type:
    print(result)
```

Cet exercice met en lumière la puissance des opérations CRUD, des fonctions d'agrégation et des requêtes sur documents imbriqués dans MongoDB. Il offre une occasion d'appliquer ces concepts à un ensemble de données ludique et engageant.