import json


class TasksSystemCurrentState:

    def __init__(self, active_tasks, archived_tasks, active_projects, archived_projects, deleted_projects):
        self.active_tasks = active_tasks
        self.archived_tasks = archived_tasks
        self.active_projects = active_projects
        self.archived_projects = archived_projects
        self.deleted_projects = deleted_projects


class Task:

    def __init__(self, id, title, created_date, journal_date, delete_date, original_data, project_id):
        self.id = id
        self.title = title
        self.created_date = created_date
        self.journal_date = journal_date
        self.delete_date = delete_date
        self.original_data = original_data
        self.project_id = project_id


class Project:

    def __init__(self, id, title, created_date, journal_date, delete_date, original_data):
        self.id = id
        self.title = title
        self.created_date = created_date
        self.journal_date = journal_date
        self.delete_date = delete_date
        self.original_data = original_data


def create_task_from_json(json_task):
    return Task(
        json_task.get('id'),
        json_task.get('title'),
        json_task.get('createdDate'),
        json_task.get('journalDate'),
        json_task.get('deleteDate'),
        json.dumps(json_task),
        json_task.get('projectId')
    )


def create_project_from_json(json_project):
    return Project(
        json_project.get('id'),
        json_project.get('title'),
        json_project.get('createdDate'),
        json_project.get('journalDate'),
        json_project.get('deleteDate'),
        json.dumps(json_project)
    )


def extract_current_state_from_backup_file(file_json_content):
    json_data = file_json_content['data']
    all_projects = [create_project_from_json(json_project) for json_project in json_data['projects']]
    all_tasks = [create_task_from_json(json_task) for json_task in json_data['tasks']]

    active_tasks = [task for task in all_tasks if task.delete_date is None and task.journal_date is None]
    archived_tasks = [task for task in all_tasks if task.journal_date is not None]
    active_projects = [project for project in all_projects if
                       project.delete_date is None and project.journal_date is None]
    archived_projects = [project for project in all_projects if project.journal_date is not None]
    deleted_projects = [project for project in all_projects if project.delete_date is not None]

    return TasksSystemCurrentState(active_tasks, archived_tasks, active_projects, archived_projects, deleted_projects)