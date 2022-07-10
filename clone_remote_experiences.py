import subprocess
from pathlib import Path
from typing import Dict

import tomli


def diff_remote_experiences(
    old_experiences: Dict[str, str], new_experiences: Dict[str, str]
) -> Dict[str, str]:
    # We don't care about anything that is only in old experiences
    # Remove anything that is only in new_experiences
    new_experience_keys = set(new_experiences.keys())
    old_experience_keys = set(old_experiences.keys())
    modified_experiences = new_experience_keys - old_experience_keys
    for key in new_experience_keys & old_experience_keys:
        if new_experiences[key] != old_experiences[key]:
            modified_experiences.add(key)
    return {key: new_experiences[key] for key in modified_experiences}


def clone_remote_experiences(
    experiences: Dict[str, Dict[str, str]], experiences_dir: Path
):
    # Git clone each experience value in experiences
    for name, data in experiences.items():
        url = data["url"]
        commit = data["commit"]
        repository_dir = experiences_dir / name
        output = subprocess.run(["git", "clone", url, str(repository_dir)])
        # Print status code
        if output.returncode != 0:
            raise RuntimeError(f"Failed to clone {url}")
        subprocess.run(["git", "checkout", commit], cwd=str(repository_dir))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "path",
        type=Path,
        help="Path to directory with experiences and experiences.toml",
        nargs="?",
        default=Path("./"),
    )
    parser.add_argument(
        "--since", type=Path, help="Last experiences/experiences.toml directory"
    )

    args = parser.parse_args()

    with open(args.path / "experiences.toml", "rb") as experiences_file:
        remote_experiences = tomli.load(experiences_file)
    experiences_dir = args.path / "experiences"
    local_experiences = [path.name for path in experiences_dir.glob("*")]

    clone_remote_experiences(remote_experiences, experiences_dir)

    paths = [
        str(experiences_dir / key)
        for key in list(remote_experiences.keys()) + local_experiences
    ]

    print("\n".join(paths))
