# Exercice 1: Importation et Création de la Collection

# Exercice 2: Analyse des Données
### Instructions

1. Comptez le nombre total de passagers.
```db.Passengers.countDocuments({})```
2. Trouvez combien de passagers ont survécu.
```db.Passengers.countDocuments({ Survived: 1 })```
3. Trouvez le nombre de passagers femmes.
```db.Passengers.countDocuments({ Sex: "female" })```
4. Trouvez le nombre de passagers avec au moins 3 enfants.
```db.Passengers.countDocuments({ Parch: { $gte: 3 } })```

# Exercice 3: Mise à Jour de Données

**Objectif :** Corriger ou ajouter des informations à certains documents.
### Instructions

1. Mettez à jour les documents pour lesquels le port d'embarquement est manquant, en supposant qu'ils sont montés à bord à Southampton.
```
db.Passengers.updateMany(
  { Embarked: { $exists: false } },
  { $set: { Embarked: "S" } }
)
```
2. Ajoutez un champ `rescued` avec la valeur `true` pour tous les passagers qui ont survécu.
```
db.Passengers.updateMany(
  { Survived: 1 },
  { $set: { rescued: true } }
)
```

# Exercice 4: Requêtes Complexes

**Objectif :** Effectuer des requêtes plus complexes pour analyser les données.
### Instructions

1. Sélectionnez les noms des 10 passagers les plus jeunes.
```
db.Passengers.find({})
  .sort({ Age: 1 })
  .limit(10)
  .forEach(doc => print(doc.Name));

```

2. Identifiez les passagers qui n'ont pas survécu et qui étaient dans la 2e classe.
```
db.Passengers.find({ Survived: 0, Pclass: 2 }).forEach(doc => printjson(doc));
```

# Exercice 5: Suppression de Données

**Objectif :** Supprimer des données spécifiques de la base de données.
### Instructions

Supprimez les enregistrements des passagers qui n'ont pas survécu et dont l'âge est inconnu.
```
db.Passengers.deleteMany({ Survived: 0, Age: { $exists: false } })
```

# Exercice 6: Mise à Jour en Masse

**Objectif :** Augmenter l'âge de tous les passagers de 1 an.
### Instructions

1. Utilisez une opération de mise à jour pour augmenter la valeur du champ `Age` de 1 pour tous les documents.
```
db.Passengers.updateMany(
  {},
  { $inc: { Age: 1 } }
)
```

# Exercice 7: Suppression Conditionnelle

**Objectif :** Supprimer les enregistrements des passagers qui n'ont pas de numéro de billet (`Ticket`).
### Instructions

1. Supprimez tous les documents où le champ `Ticket` est absent ou vide.
```
db.Passengers.deleteMany({ Ticket: { $exists: false } })
```

## Bonus: Utiliser les REGEX

**Objectif :** Utiliser une regex pour trouver tous les passagers selon une condition.
### Instructions

1. Utiliser une regex pour trouver tous les passagers qui porte le titre de `Dr.`