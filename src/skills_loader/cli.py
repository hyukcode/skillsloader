import typer

from .installer import (
    sync,
    install,
    remove,
    get_skills,
)


app = typer.Typer()



@app.command()
def list():

    """
    List local skills
    """

    for skill in get_skills():

        typer.echo(
            skill.name
        )



@app.command()
def install_skill(
    name:str
):

    install(name)



@app.command()
def remove_skill(
    name:str
):

    remove(name)



@app.command()
def sync_all():
    sync()



if __name__=="__main__":

    app()