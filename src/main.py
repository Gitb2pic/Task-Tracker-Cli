# -*- coding: utf-8 -*-
# This file is part of the Task Manager project.   
import argparse
from src.controllers.config import status, create_task, listing_all_tasks, update_task, delete_task, print_task_statuses, change_task_status, print_task_by_status

parser = argparse.ArgumentParser(description="Gestionnaire de tâches")
parser.add_argument('action', choices=['create', 'list', 'update', 'delete', 'status', 'change_status', 'print_by_status'], help="Action à effectuer sur les tâches")
parser.add_argument('--task_id', type=int, help="ID de la tâche à mettre à jour ou supprimer")
parser.add_argument('--task_name', type=str, help="Nom de la tâche à créer ou mettre à jour")
parser.add_argument('--new_status_id', type=int, help="Nouvel ID de statut pour changer le statut d'une tâche")
args = parser.parse_args()


def main():
    """
    Gestionnaire de tâches en ligne de commande
    Ce script permet de créer, lister, mettre à jour, supprimer des tâches et de gérer leurs statuts.
    """
    if args.action == 'create':
        if not args.task_name:
            print("Veuillez fournir un nom de tâche avec --task_name.")
            return
        create_task(args.task_name)
    elif args.action == 'list':
        listing_all_tasks()
    elif args.action == 'update':
        if not args.task_id or not args.task_name:
            print("Veuillez fournir l'ID de la tâche avec --task_id et le nouveau nom avec --task_name.")
            return
        update_task(args.task_id, args.task_name)
    elif args.action == 'delete':
        if not args.task_id:
            print("Veuillez fournir l'ID de la tâche à supprimer avec --task_id.")
            return
        delete_task(args.task_id)
    elif args.action == 'status':
        print_task_statuses()
    elif args.action == 'change_status':
        if not args.task_id or args.new_status_id is None:
            print("Veuillez fournir l'ID de la tâche avec --task_id et le nouvel ID de statut avec --new_status_id.")
            return
        change_task_status(args.task_id, args.new_status_id)
    elif args.action == 'print_by_status':
        if not args.task_name:
            print(f"Veuillez fournir le statut de la tâche avec --task_name. Statuts disponibles : {status}")
            return
        print_task_by_status(args.task_name)
if __name__ == "__main__":
    main()
