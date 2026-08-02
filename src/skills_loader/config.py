from pathlib import Path


HOME = Path.home()


SKILL_SOURCE = (
    HOME /
    "agent-skills"
)


TARGETS = {

    "claude":
        HOME /
        ".claude" /
        "skills",

    "codex":
        HOME /
        ".codex" /
        "skills",

    "cursor":
        HOME /
        ".cursor" /
        "skills"

}