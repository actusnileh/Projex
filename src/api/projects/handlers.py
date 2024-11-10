from fastapi import (
    Depends,
    status,
)
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from api.projects.schemas import (
    CreateProjectRequestSchema,
    CreateProjectResponseSchema,
)
from api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.projects import CreateProjectCommand
from logic.init import init_container
from logic.mediator import Mediator


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
    container=Depends(init_container),
):
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
