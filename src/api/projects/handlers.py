from fastapi import (
    Depends,
    status,
)
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from punq import Container

from api.projects.schemas import (
    CreateProjectRequestSchema,
    CreateProjectResponseSchema,
    CreateTaskRequestSchema,
    CreateTaskResponseSchema,
    ProjectDetailSchema,
)
from api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.projects import (
    CreateProjectCommand,
    CreateTaskCommand,
)
from logic.init import init_container
from logic.mediator import Mediator
from logic.queries.projects import GetProjectDetailQuery


router = APIRouter(
    tags=["Projects"],
)


@router.post(
    "/",
    responses={
        status.HTTP_201_CREATED: {"model": CreateProjectResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт создаёт новый проект, если проект с таким названием существует, то возвращается 400 ошибка.",
)
async def create_project_handler(
    schema: CreateProjectRequestSchema,
    container: Container = Depends(init_container),
) -> CreateProjectResponseSchema:
    """Создать новый проект."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        project, *_ = await mediator.handle_command(
            CreateProjectCommand(title=schema.title),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return CreateProjectResponseSchema.from_entity(project)


@router.post(
    "/{project_oid}/tasks",
    responses={
        status.HTTP_201_CREATED: {"model": CreateTaskResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт добавляет новую задачу в проект с переданным ObjectID.",
)
async def create_task_handler(
    project_oid: str,
    schema: CreateTaskRequestSchema,
    container: Container = Depends(init_container),
) -> CreateTaskResponseSchema:
    """Добавить новое задание в проект."""
    mediator: Mediator = container.resolve(Mediator)
    try:
        task, *_ = await mediator.handle_command(
            CreateTaskCommand(
                title=schema.title,
                text=schema.text,
                project_oid=project_oid,
            ),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return CreateTaskResponseSchema.from_entity(task)


@router.get(
    "/{project_oid}/",
    status_code=status.HTTP_200_OK,
    description="Получить информацию о проекте и всех задачах в нём.",
    responses={
        status.HTTP_200_OK: {"model": ProjectDetailSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_project_with_tasks_handler(
    project_oid: str,
    container: Container = Depends(init_container),
) -> ProjectDetailSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        project = await mediator.handle_query(
            GetProjectDetailQuery(project_oid=project_oid),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return ProjectDetailSchema.from_entity(project)
