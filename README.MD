# 📋 Task Tracker CLI

**Task Tracker CLI** est une application en ligne de commande permettant de gérer vos tâches quotidiennes. Ce projet vous aidera à pratiquer des compétences essentielles telles que la manipulation du système de fichiers, la gestion des entrées utilisateur et la création d'une interface CLI simple.([roadmap.sh][2])

## 🚀 Fonctionnalités

* Ajouter, mettre à jour et supprimer des tâches
* Marquer une tâche comme *en cours* ou *terminée*
* Lister toutes les tâches
* Lister les tâches par statut : *à faire*, *en cours*, *terminée*([GitHub][3], [DEV Community][4])

## 🧱 Spécifications techniques

* L'application doit être exécutable depuis la ligne de commande
* Utiliser des arguments positionnels pour accepter les entrées utilisateur
* Stocker les tâches dans un fichier JSON local (créé s'il n'existe pas)
* Utiliser les modules natifs du langage choisi pour interagir avec le système de fichiers
* Ne pas utiliser de bibliothèques ou frameworks externes
* Gérer les erreurs et les cas limites de manière appropriée([GitHub][3], [roadmap.sh][2])

## 🗃️ Structure des données

Chaque tâche est représentée par un objet avec les propriétés suivantes :

* `id` : identifiant unique
* `description` : description courte de la tâche
* `status` : statut de la tâche (`todo`, `in-progress`, `done`)
* `createdAt` : date et heure de création
* `updatedAt` : date et heure de la dernière mise à jour([roadmap.sh][2])

## 📦 Commandes disponibles

```bash
# Ajouter une nouvelle tâche
task-cli add "Acheter des légumes"

# Mettre à jour une tâche
task-cli update 1 "Acheter des légumes et cuisiner le dîner"

# Supprimer une tâche
task-cli delete 1

# Marquer une tâche comme en cours
task-cli mark-in-progress 1

# Marquer une tâche comme terminée
task-cli mark-done 1

# Lister toutes les tâches
task-cli list

# Lister les tâches par statut
task-cli list todo
task-cli list in-progress
task-cli list done
```

## 🛠️ Mise en route

1. Choisissez un langage de programmation (par exemple, Python, JavaScript, Go)
2. Créez un fichier `tasks.json` dans le répertoire courant
3. Implémentez les fonctionnalités en suivant les spécifications ci-dessus
4. Testez chaque fonctionnalité individuellement
5. Ajoutez des messages d'erreur clairs pour les cas limites

## 📚 Ressources utiles

* [Spécifications officielles du projet sur roadmap.sh](https://roadmap.sh/projects/task-tracker)
* [Exemples de solutions communautaires](https://roadmap.sh/projects/task-tracker/solutions)

