from domain.entities.projects import (
    Project,
    Task,
)


def convert_tasks_to_document(task: Task) -> dict:
    return {
        "oid": task.oid,
        "title": task.title.as_generic_type(),
        "text": task.text.as_generic_type(),
        "created_at": task.created_at,
    }


def convert_project_to_document(project: Project) -> dict:
    return {
        "oid": project.oid,
        "title": project.title.as_generic_type(),
        "created_at": project.created_at,
        "tasks": [convert_tasks_to_document(task) for task in project.tasks],
    }
