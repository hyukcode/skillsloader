from typing import List, Optional

import typer

from .config import TARGETS
from .installer import (
    sync,
    install,
    remove,
    remove_from,
    get_skills,
    get_target_skills,
    get_common_skills,
    copy_skill,
)


app = typer.Typer()



def _check_agent(agent):

    if agent not in TARGETS:

        raise typer.BadParameter(
            f"unknown agent: {agent} (choose from {', '.join(TARGETS)})"
        )



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
def view(
    agent: Optional[str] = typer.Option(
        None,
        "--agent",
        help="Show only this agent"
    )
):

    """
    Show skills installed in each agent
    """

    if agent is not None:
        _check_agent(agent)

    agents = [agent] if agent else sorted(TARGETS)

    for name in agents:

        skills = get_target_skills(name)

        typer.echo(
            f"{name}: {', '.join(skills) if skills else '(none)'}"
        )

    if agent is None:

        common = get_common_skills()

        typer.echo(
            f"common: {', '.join(common) if common else '(none)'}"
        )



@app.command()
def install_skill(
    name:str
):

    install(name)



@app.command()
def remove_skill(
    name: str,
    agent: Optional[str] = typer.Option(
        None,
        "--agent",
        help="Remove from only this agent (default: all)"
    )
):

    """
    Remove a skill from all agents, or from one agent
    """

    if agent is not None:

        _check_agent(agent)

        remove_from(agent, name)

    else:

        remove(name)



@app.command()
def remove_common(
    yes: bool = typer.Option(
        False,
        "--yes",
        help="Skip confirmation"
    )
):

    """
    Remove all skills that exist in every agent
    """

    common = get_common_skills()

    if not common:

        typer.echo(
            "no common skills"
        )
        return

    typer.echo(
        "common skills: " + ", ".join(common)
    )

    if not yes:

        if not typer.confirm(
            "remove all of them?"
        ):
            return

    for skill_name in common:

        remove(skill_name)



@app.command()
def copy(
    skills: List[str] = typer.Argument(
        ...,
        help="Skill name(s) to copy"
    ),
    from_agent: str = typer.Option(
        ...,
        "--from",
        help="Source agent"
    ),
    to_agent: str = typer.Option(
        ...,
        "--to",
        help="Destination agent"
    )
):

    """
    Copy skill(s) from one agent to another
    """

    _check_agent(from_agent)

    _check_agent(to_agent)

    for skill_name in skills:

        copy_skill(
            skill_name,
            from_agent,
            to_agent
        )



@app.command()
def sync_all():
    sync()



if __name__=="__main__":

    app()
