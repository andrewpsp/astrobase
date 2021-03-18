import docker
import typer
import yaml

from astrobase_cli import __version__ as version
from astrobase_cli import apply, destroy, profile
from utils.config import AstrobaseConfig, AstrobaseDockerConfig

astrobase_apply = apply.Apply()
astrobase_destroy = destroy.Destroy()
docker_client = docker.from_env()
name = f"🚀 Astrobase CLI {version} 🧑‍🚀"

app = typer.Typer(name=name)
app.add_typer(profile.app, name="profile")


@app.callback()
def main_callback():
    pass


main_callback.__doc__ = name


@app.command()
def version():
    """
    Print the Astrobase CLI version.
    """
    typer.echo(name)


@app.command()
def init(astrobase_container_version: str = "latest"):
    """
    Initialize Astrobase.
    """
    astrobase_config = AstrobaseConfig()
    typer.echo("Initializing Astrobase ... ")
    if not astrobase_config.current_profile:
        typer.echo(
            "No profile is set! set a profile with: export "
            f"{astrobase_config.ASTROBASE_PROFILE}=<my-profile-name>"
        )
        return
    astrobase_docker_config = AstrobaseDockerConfig(
        container_version=astrobase_container_version,
        astrobase_config=astrobase_config,
    )
    typer.echo("Starting Astrobase server ... ")
    docker_client.containers.run(
        image=astrobase_docker_config.image,
        ports=astrobase_docker_config.ports,
        environment=astrobase_docker_config.environment,
        volumes=astrobase_docker_config.volumes,
        auto_remove=astrobase_docker_config.auto_remove,
        detach=astrobase_docker_config.detach,
        name=astrobase_docker_config.name,
    )
    typer.echo("Astrobase initialized")


@app.command()
def apply(astrobase_yaml_path: str = typer.Option(..., "-f")):
    """
    Apply clusters, resources, and workflows.
    """
    with open(astrobase_yaml_path, "r") as f:
        data = yaml.safe_load(f)

        clusters = data.get("clusters") or []
        resources = data.get("resources") or []
        workflows = data.get("workflows") or []  # TODO!

        astrobase_apply.apply_clusters(clusters)
        astrobase_apply.apply_resources(resources)
        astrobase_apply.apply_workflows(workflows)


@app.command()
def destroy(astrobase_yaml_path: str = typer.Option(..., "-f")):
    """
    Destroy clusters, resources, and workflows.
    """
    with open(astrobase_yaml_path, "r") as f:
        data = yaml.safe_load(f)

        clusters = data.get("clusters") or []
        resources = data.get("resources") or []
        workflows = data.get("workflows") or []  # TODO!

        astrobase_destroy.destroy_clusters(clusters)
        astrobase_destroy.destroy_resources(resources)
        astrobase_destroy.destroy_workflows(workflows)


if __name__ == "__main__":
    app()
