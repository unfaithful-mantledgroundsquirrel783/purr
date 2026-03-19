import shutil

import typer

from kitten_cli.config import MODEL_REGISTRY, MODELS_DIR


def is_model_downloaded(alias: str) -> bool:
    model_dir = MODELS_DIR / alias
    return model_dir.exists() and any(model_dir.iterdir())


def install_model(alias: str) -> None:
    if alias not in MODEL_REGISTRY:
        typer.echo(
            f"Unknown model alias '{alias}'. Available: {', '.join(MODEL_REGISTRY)}",
            err=True,
        )
        raise typer.Exit(1)

    repo_id = MODEL_REGISTRY[alias]
    dest = MODELS_DIR / alias
    dest.mkdir(parents=True, exist_ok=True)

    typer.echo(f"Downloading model '{alias}' from {repo_id} ...")
    from kittentts import KittenTTS  # type: ignore
    KittenTTS(repo_id, cache_dir=str(dest))
    typer.echo(f"Model '{alias}' installed to {dest}")


def list_models() -> None:
    for alias in MODEL_REGISTRY:
        status = "[installed]" if is_model_downloaded(alias) else "[not installed]"
        typer.echo(f"  {alias:<12} {status}")


def remove_model(alias: str) -> None:
    if alias not in MODEL_REGISTRY:
        typer.echo(
            f"Unknown model alias '{alias}'. Available: {', '.join(MODEL_REGISTRY)}",
            err=True,
        )
        raise typer.Exit(1)

    model_dir = MODELS_DIR / alias
    if not model_dir.exists():
        typer.echo(f"Model '{alias}' is not installed.", err=True)
        raise typer.Exit(1)

    shutil.rmtree(model_dir)
    typer.echo(f"Model '{alias}' removed.")
