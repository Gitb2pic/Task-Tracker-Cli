from src.models.task import Task
from tabulate import tabulate
import json
import os

# chemin  vers src/Data/data.json
data_dir = os.path.join(os.path.dirname(__file__), "../Data")
data_file = os.path.join(data_dir,"data.json")
os.makedirs(data_dir, exist_ok=True)


def find_task(task_id):
    with open(data_file, "r") as file:
        tasks = json.load(file)

    # Tri des tâches par task_id (au cas où elles ne seraient pas triées)
    tasks.sort(key=lambda x: x["task_id"])

    # Recherche binaire
    low = 0
    high = len(tasks) - 1

    while low <= high:
        mid = (low + high) // 2
        current_id = tasks[mid]["task_id"]

        if current_id == task_id:
            return tasks[mid]
        elif current_id < task_id:
            low = mid + 1
        else:
            high = mid - 1

    return None  # Tâche non trouvée

def create_task(task_name):
    # charger ou initialiser la liste des taches
    if not os.path.exists(data_file):
        with open(data_file, "w") as file:
            json.dump([], file)
    
    with open(data_file, "r") as file:
        try:
            tasks = json.load(file)
        except json.JSONDecodeError:
            tasks = []
    #Trouver le prochain ID
    if tasks:
        max_id =  max((task["task_id"] for task in tasks), default=0)
    else:
        max_id = 0

    new_id = max_id + 1
    
    #créer la nouvelle tache avec l'ID  auto
    task = Task(new_id, task_name)
    tasks.append(task.__dict__)
    
    #Enregistrer les tâches mises à jour 
    with open(data_file, "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Tâche '{task_name}' ajoutée avec ID : {new_id}")

#Create a function to liste all information about tasks

def listing_all_tasks():
    with open(data_file, 'r') as file:
        tasks = json.load(file)

    if not tasks:
        print("Aucune tâche enregistrée.")
        return

    table = []
    for task in tasks:
        if not task['is_visible'] == False:
            table.append([task['task_id'], task['task_name'],task['task_status']])

    print(tabulate(table, headers=["ID", "Nom","status"], tablefmt="fancy_grid"))


# Create a function to update an information about task
def update_task(task_id, task_name):
    task = find_task(task_id)
    if task is None:
        print(f"Tâche avec ID {task_id} non trouvée.")
        return
    task['task_name'] = task_name
    
    with open(data_file, 'r') as file:
        tasks = json.load(file)

    # Recherche binaire pour trouver l'index de la tâche à mettre à jour
    low = 0
    high = len(tasks) - 1

    while low <= high:
        mid = (low + high) // 2
        if tasks[mid]['task_id'] == task_id:
            tasks[mid] = task
            break
        elif tasks[mid]['task_id'] < task_id:
            low = mid + 1
        else:
            high = mid - 1

    with open(data_file, 'w') as file:
        json.dump(tasks, file, indent=4)

    print(f"Tâche avec ID {task_id} mise à jour.")

# TODO Delete a task
def delete_task(task_id): 

    task = find_task(task_id)  # -1 pour ajuster l'ID à l'index de la liste

    if task is None:
        print(f"Tâche avec ID {task_id} non trouvée.")
        return
    task['is_visible'] = False  # Marquer la tâche comme non visible
    with open(data_file, 'r') as file:
        tasks = json.load(file)
    # Recherche binaire pour trouver l'index de la tâche à supprimer
    tasks[task_id] = task

    with open(data_file, 'w') as file:
        json.dump(tasks, file, indent=4)

    print(f"Tâche avec ID {task_id} supprimée.")

# TODO  Marquer une tâche comme en cours


#TODO // Lister les tâches par statut



#Test
if __name__== "__main__":
    # create_task("Test Task 1")
    # create_task("Test Task 2")
    # listing_all_tasks()
    #  update_task(1, "Updated Task 1")
    # listing_all_tasks()
     delete_task(1)
    # listing_all_tasks()