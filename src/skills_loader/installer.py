from pathlib import Path
import shutil

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


        shutil.copytree(
            source,
            target
        )


        print(
            f"[OK] {agent}: {skill_name}"
        )



def get_target_skills(agent):

    """
    List skill names installed for a given agent
    """

    target_root = TARGETS.get(agent)

    if target_root is None:
        return []

    if not target_root.exists():
        return []

    return sorted(
        x.name
        for x in target_root.iterdir()
        if x.is_dir()
    )



def get_common_skills():

    """
    Skills present in every agent (the intersection)
    """

    common = None

    for agent in TARGETS:

        names = set(
            get_target_skills(agent)
        )

        common = names if common is None else (common & names)

    return sorted(common or [])



def remove_from(agent, skill_name):

    target = (
        TARGETS.get(agent, Path()) /
        skill_name
    )


    if target.is_symlink() or target.exists():

        if target.is_symlink():
            target.unlink()

        else:
            shutil.rmtree(target)


        print(
            f"removed {agent}: {skill_name}"
        )

    else:
        print(
            f"not found in {agent}: {skill_name}"
        )



def copy_skill(skill_name, from_agent, to_agent):

    src_root = TARGETS.get(from_agent)

    dst_root = TARGETS.get(to_agent)

    if src_root is None or dst_root is None:
        print(
            "unknown agent"
        )
        return


    src = (
        src_root /
        skill_name
    )

    dst = (
        dst_root /
        skill_name
    )


    if not src.exists() or not src.is_dir():
        print(
            f"skill not found in {from_agent}: {skill_name}"
        )
        return


    dst.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    if dst.is_symlink() or dst.exists():

        if dst.is_symlink():
            dst.unlink()

        else:
            shutil.rmtree(dst)


    shutil.copytree(
        src,
        dst
    )


    print(
        f"[OK] {from_agent} -> {to_agent}: {skill_name}"
    )



def remove(skill_name):

    for agent in TARGETS:

        remove_from(
            agent,
            skill_name
        )



def sync():

    for skill in get_skills():

        install(
            skill.name
        )
