# Exercice 1: Création d'une Base de Données et d'une Collection

# Exercice 2: Insertion de Données

# Exercice 3: Lecture de Données:
- Pokemon type feu : 
```
db.Pokemons.find({
  $or: [
    { "Type 1": "Fire" },
    { "Type 2": "Fire" }
  ]
})
```

- Information Pikachu :
```
db.Pokemons.find({
    Name:"Pikachu"
})
```


# Exercice 4: Mise à Jour de Données
```
db.Pokemons.updateOne({
    'Name': 'Pikachu'},
    {'$set': {'Max CP': 901}
})
```

Verif
```
db.Pokemons.find({
    Name:"Pikachu"
})
```
# Exercice 5: Suppression d'Éléments
```
db.Pokemons.delete_one({ Name: "Bulbasaur" })
```

Verif :
```
db.Pokemons.find({
    Name:"Bulbasaur"
})
```


