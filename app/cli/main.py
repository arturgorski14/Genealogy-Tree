import click
import httpx

BASE_URL = "http://localhost:8000/people/"


# ========== ROOT ==========
@click.group()
@click.option("--host", default=BASE_URL, help="API base URL")
@click.pass_context
def cli(ctx, host):
    ctx.ensure_object(dict)
    ctx.obj["BASE_URL"] = host


# ========== COMMANDS ==========


@cli.command()
@click.argument("pretty-print", default=False)
@click.pass_context
def list(ctx, pretty_print):
    """List all people"""
    url = ctx.obj["BASE_URL"]
    r = httpx.get(url)
    r.raise_for_status()

    if not pretty_print:
        click.echo(r.json())
        return
    for person_result in r.json():
        click.echo(person_result)


@cli.command()
@click.argument("uid")
@click.pass_context
def get(ctx, uid):
    """Get person by ID"""
    url = ctx.obj["BASE_URL"]
    r = httpx.get(f"{url}{uid}")

    if r.status_code == 404:
        click.echo("Person not found")
        return

    click.echo(r.json())


@cli.command()
@click.argument("name")
@click.pass_context
def create(ctx, name):
    """Create person"""
    url = ctx.obj["BASE_URL"]
    r = httpx.post(url, json={"name": name})
    r.raise_for_status()
    click.echo(r.json())


@cli.command(name="add-parent")
@click.argument("parent_id")
@click.argument("child_id")
@click.pass_context
def add_parent(ctx, parent_id, child_id):
    """Add parent-child relationship"""
    url = ctx.obj["BASE_URL"]

    r = httpx.post(
        f"{url}relationships/parent-child",
        json={
            "parent_id": parent_id,
            "child_id": child_id,
        },
    )

    if r.status_code == 409:
        click.echo("Cycle detected!")
        return

    click.echo("Relationship created")


@cli.command()
@click.argument("uid")
@click.pass_context
def delete(ctx, uid):
    """Delete person"""
    url = ctx.obj["BASE_URL"]

    r = httpx.delete(f"{url}{uid}")

    if r.status_code == 404:
        click.echo("Person not found")
        return

    click.echo("Deleted")


if __name__ == "__main__":
    cli()
