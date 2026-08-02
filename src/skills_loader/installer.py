from pathlib import Path
import shutil
import os

from .config import (
    SKILL_SOURCE,
    TARGETS
)



def get_skills():

    if not SKILL_SOURCE.exists():
        return []

    return [
        x for x in SKILL_SOURCE.iterdir()
        if x.is_dir()
    ]



def install(skill_name):

    source = (
        SKILL_SOURCE /
        skill_name
    )

    if not source.exists():
        print(
            "skill not found:",
            skill_name
        )
        return


    for agent,target_root in TARGETS.items():

        target_root.mkdir(
            parents=True,
            exist_ok=True
        )


        target = (
            target_root /
            skill_name
        )


        if target.is_symlink() or target.exists():

            if target.is_symlink():
                target.unlink()

            else:
                shutil.rmtree(target)


        os.symlink(
            source,
            target,
            target_is_directory=True
        )


        print(
            f"[OK] {agent}: {skill_name}"
        )



def remove(skill_name):

    for agent,target_root in TARGETS.items():

        target = (
            target_root /
            skill_name
        )


        if target.is_symlink() or target.exists():

            if target.is_symlink():
                target.unlink()

            else:
                shutil.rmtree(target)


            print(
                f"removed {agent}"
            )



def sync():

    for skill in get_skills():

        install(
            skill.name
        )
