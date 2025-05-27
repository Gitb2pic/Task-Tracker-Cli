class Task:
    def __init__(self, task_id, task_name, task_description, task_status="Not done", is_visible=True):

        self.task_id = task_id
        self.task_name = task_name
        self.task_description = task_description
        self.task_status = task_status
        self.is_visible = is_visible

