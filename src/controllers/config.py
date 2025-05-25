from src.models.task import Task
import json
import os
#
def create_task(task_name, task_description):
    # chemin  vers src/Data/data.json
    data_dir = os.path.join(os.path.dirname(__file__), "../Data")
    data_file = os.path.join(data_dir,"data.json")
    os.makedirs(data_dir, exist_ok=True)

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
    task = Task(new_id, task_name, task_description)
    tasks.append(task.__dict__)
    
    #Enregistrer les tâches mises à jour 
    with open(data_file, "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Tâche '{task_name}' ajoutée avec ID : {new_id}")

#Test
if __name__== "__main__":
    create_task("Apprendre python", "Revoir les fonctions et les modules")        

