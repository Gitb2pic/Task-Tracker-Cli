from src.models.task import Task
from tabulate import tabulate
import json
import os

data_dir = os.path.join(os.path.dirname(__file__), "../Data")
data_file = os.path.join(data_dir,"data.json")
os.makedirs(data_dir, exist_ok=True)
# Liste des statuts possibles pour les tâches
status = ("Not done", "In progress", "Done", "Archived")


# Fonctions d'aide (privées)

def _robust_sort_key(task_item):
    """Clé de tri robuste pour les tâches, gérant les types et absences de task_id."""
    if isinstance(task_item, dict):
        val = task_item.get("task_id")
        # S'assurer que l'ID est un nombre comparable
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            return val
    return float('inf') # Les éléments non-conformes ou sans ID numérique sont placés à la fin

def _load_tasks():
    """Charge les tâches depuis le fichier JSON, les trie et gère les erreurs."""
    if not os.path.exists(data_file):
        return []
    try:
        with open(data_file, "r", encoding='utf-8') as file:
            tasks = json.load(file)
            if not isinstance(tasks, list): # S'assurer que le contenu est une liste
                print(f"Erreur: Le contenu de {data_file} n'est pas une liste. Une liste vide sera utilisée.")
                return []
            tasks.sort(key=_robust_sort_key)
            return tasks
    except json.JSONDecodeError:
        print(f"Erreur: Fichier de données {data_file} corrompu ou malformé. Une liste vide sera utilisée.")
        # Optionnel: sauvegarder le fichier corrompu
        # try:
        #     os.rename(data_file, data_file + f".corrupted_{int(time.time())}")
        # except OSError as e_rename:
        #     print(f"Impossible de renommer le fichier corrompu: {e_rename}")
        return []
    except Exception as e:
        print(f"Une erreur inattendue est survenue lors du chargement des tâches: {e}")
        return []

def _save_tasks(tasks):
    """Sauvegarde la liste des tâches dans le fichier JSON de manière atomique."""
    tasks.sort(key=_robust_sort_key) # Maintenir l'ordre dans le fichier
    temp_data_file = data_file + ".tmp"
    try:
        with open(temp_data_file, "w", encoding='utf-8') as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)
        os.replace(temp_data_file, data_file)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des tâches: {e}")
        if os.path.exists(temp_data_file):
            try:
                os.remove(temp_data_file)
            except OSError as e_remove:
                print(f"Erreur additionnelle lors de la suppression du fichier temporaire: {e_remove}")

def _find_task_by_id_and_get_index(tasks_list, task_id):
    """Recherche une tâche par ID et retourne la tâche et son index."""
    # Note: tasks_list est supposée être triée par _load_tasks
    low = 0
    high = len(tasks_list) - 1
    while low <= high:
        mid = (low + high) // 2
        current_task = tasks_list[mid]

        if not isinstance(current_task, dict):
            # Gérer les éléments malformés (devraient être à la fin à cause du tri)
            high = mid - 1 
            continue

        current_id = current_task.get("task_id")
        if not isinstance(current_id, (int, float)) or isinstance(current_id, bool): # ID non numérique ou manquant
             # Devrait être à la fin à cause du tri avec float('inf')
            high = mid - 1
            continue
            
        if current_id == task_id:
            return current_task, mid
        elif current_id < task_id:
            low = mid + 1
        else:
            high = mid - 1
    return None, -1

# Fonctions publiques de l'API

def find_task(task_id):
    """Trouve une tâche par son ID."""
    tasks = _load_tasks()
    task, _ = _find_task_by_id_and_get_index(tasks, task_id)
    return task

def create_task(task_name):
    """Crée une nouvelle tâche."""
    tasks = _load_tasks()
    
    max_id = 0
    if tasks:
        valid_ids = [
            t.get("task_id") for t in tasks 
            if isinstance(t, dict) and isinstance(t.get("task_id"), (int, float)) and not isinstance(t.get("task_id"), bool)
        ]
        if valid_ids:
            max_id = max(valid_ids, default=0)

    new_id = max_id + 1
    
    # Assumer que la classe Task gère les valeurs par défaut (status, is_visible)
    new_task_obj = Task(new_id, task_name)
    # Il serait préférable d'avoir une méthode new_task_obj.to_dict() dans la classe Task
    tasks.append(new_task_obj.__dict__) 
    
    _save_tasks(tasks)
    print(f"Tâche '{task_name}' ajoutée avec ID : {new_id}")

def listing_all_tasks():
    """Liste toutes les tâches visibles."""
    tasks = _load_tasks()

    if not tasks:
        print("Aucune tâche enregistrée.")
        return

    table_data = []
    for task in tasks:
        if isinstance(task, dict) and task.get('is_visible', True): # Afficher si visible ou si la clé manque (par défaut visible)
            table_data.append([
                task.get('task_id', 'N/A'), 
                task.get('task_name', 'Sans nom'), 
                task.get('task_status', 'Indéfini') # Assumer que 'task_status' vient de Task
            ])

    if not table_data:
        print("Aucune tâche visible à afficher.")
        return
        
    print(tabulate(table_data, headers=["ID", "Nom", "Status"], tablefmt="fancy_grid"))

def update_task(task_id, new_task_name):
    """Met à jour le nom d'une tâche existante."""
    tasks = _load_tasks()
    _, index = _find_task_by_id_and_get_index(tasks, task_id)

    if index == -1:
        print(f"Tâche avec ID {task_id} non trouvée.")
        return

    tasks[index]['task_name'] = new_task_name
    # Optionnel: mettre à jour un champ 'date_modification'
    
    _save_tasks(tasks)
    print(f"Tâche avec ID {task_id} mise à jour.")

def delete_task(task_id): 
    """Marque une tâche comme supprimée (invisible)."""
    tasks = _load_tasks()
    _, index = _find_task_by_id_and_get_index(tasks, task_id)

    if index == -1:
        print(f"Tâche avec ID {task_id} non trouvée.")
        return

    tasks[index]['is_visible'] = False
    
    _save_tasks(tasks)
    print(f"Tâche avec ID {task_id} marquée comme supprimée.")

# TODO: Ajouter des fonctions pour changer le statut des tâches (par exemple, de 'à faire' à 'terminée').
def print_task_statuses():
    """Affiche les statuts disponibles pour les tâches."""
    print("Statuts disponibles pour les tâches :")
    for idx, stat in enumerate(status):
        print(f"{idx}: {stat}")

def change_task_status(task_id, new_status_id):
    """Change le statut d'une tâche."""
    tasks = _load_tasks()
    _, index = _find_task_by_id_and_get_index(tasks, task_id)
    if index == -1:
        print(f"Tâche avec ID {task_id} non trouvée.")
        return

    if new_status_id < 0 or new_status_id >= len(status):
        print(f"Statut invalide. Veuillez utiliser un ID de statut entre 0 et {len(status) - 1}.")
        return

    tasks[index]['task_status'] = status[new_status_id]

    _save_tasks(tasks)
    print(f"Statut de la tâche avec ID {task_id} mis à jour vers '{status[new_status_id]}'.")

    