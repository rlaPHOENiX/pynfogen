import logging
from pathlib import Path

import click

from pynfogen.helpers import open_file


@click.group()
def template():
    """Manages template files."""
    pass


@template.command()
@click.argument("name", type=str)
@click.pass_obj
def edit(obj, name: str):
    """Edit a template file. If one does not exist, one will be created."""
    log = logging.getLogger("template")
    location = Path(obj["templates"] / f"{name}.nfo")
    if not location.exists():
        log.info(f"Creating new template named {name}")
        location.parent.mkdir(exist_ok=True, parents=True)
        location.open("a").close()
    else:
        log.info(f"Opening existing template {name} for editing")
    open_file(str(location))


@template.command()
@click.argument("name", type=str)
@click.confirmation_option(prompt="Are you sure you want to delete the template?")
@click.pass_obj
def delete(obj, name: str):
    """Delete a template file."""
    log = logging.getLogger("template")
    location = Path(obj["templates"] / f"{name}.nfo")
    if not location.exists():
        raise click.ClickException(f"Template {name} does not exist.")
    location.unlink()
    log.info(f"Template {name} has been deleted.")


@template.command(name="list")
@click.pass_obj
def list_(obj):
    """List all available templates."""
    location = Path(obj["templates"])
    if not location.is_dir():
        raise click.ClickException("No templates exist.")
    for file in location.iterdir():
        print(file.stem)