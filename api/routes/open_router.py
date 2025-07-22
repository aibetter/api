from fastapi import APIRouter, Request
import json
import os

router = APIRouter(prefix="/api/v1/open-router", tags=["open-router"])


@router.get("/models")
def get_models(request: Request, name: str = None, free_only: bool = False):
    """
    Get OpenRouter models with optional filtering

    Args:
        name: Filter models by name (case-insensitive partial match)
        free_only: If True, only return completely free models
    """

    limiter = request.app.state.limiter
    limiter.limit("30/minute")(request)

    models_file = os.path.join(
        os.path.dirname(__file__), "../../data/open-router/models.json"
    )

    with open(models_file, "r", encoding="utf-8") as f:
        models = json.load(f)

    if name:
        models = [
            model for model in models if name.lower() in model.get("name", "").lower()
        ]

    if free_only:
        models = [
            model
            for model in models
            if all(
                model.get("pricing", {}).get(key, "0") == "0"
                for key in [
                    "prompt",
                    "completion",
                    "request",
                    "image",
                    "web_search",
                    "internal_reasoning",
                ]
            )
        ]

    return {"total": len(models), "models": models}
