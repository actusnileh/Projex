from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from src.api.dependencies.containers import container
from src.api.projects.schemas import (
    CreateProjectRequestSchema,
    CreateProjectResponseSchema,
)
from src.api.schemas import ErrorSchema
from src.domain.exceptions.base import ApplicationException
from src.logic.commands.projects import CreateProjectCommand
from src.logic.mediator import Mediator


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
async def create_project_handler(schema: CreateProjectRequestSchema):
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
