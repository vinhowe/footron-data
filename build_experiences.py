import subprocess
from pathlib import Path
from typing import Dict

import tomli
import json
import shutil


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


def build_experiences(experiences_dir: Path, build_dir: Path):
    if build_dir.exists():
        shutil.rmtree(build_dir)

    # Make sure build directory exists
    build_dir.mkdir(parents=True, exist_ok=True)

    # Build each experience in experiences_dir
    for experience_name in experiences_dir.glob("*"):
        experience_name = experience_name.name
        experience_dir = experiences_dir / experience_name

        # Create experience build directory
        experience_build_dir = build_dir / experience_name
        experience_build_dir.mkdir(parents=True, exist_ok=True)

        # Copy config file, either config.json or config.toml
        if (
            not (config_path := experience_dir / "config.json").exists()
            and not (config_path := experience_dir / "config.toml").exists()
        ):
            raise RuntimeError(
                f"Experience '{experience_name}' doesn't have a config file"
            )

        # Copy config file to build directory
        shutil.copy(config_path, experience_build_dir)

        # Read config data
        with open(config_path, "rb") as config_file:
            config = (json if config_path.suffix == ".json" else tomli).load(
                config_file
            )

        if (unlisted := config.get("unlisted")) is None or not unlisted:
            # Copy image files to build directory
            for image_path in (
                experience_dir / "wide.jpg",
                experience_dir / "thumb.jpg",
            ):
                if not image_path.exists():
                    raise RuntimeError(
                        f"Experience '{experience_name}' is missing image file '{image_path.name}'"
                    )
                shutil.copy(image_path, experience_build_dir)

        # Do web build
        web_dir = experience_dir / "web"
        # TODO: Move this into its own function
        if web_dir.exists():
            package_json = web_dir / "package.json"
            # Check if package.json exists, build npm project if so
            if package_json.exists():
                install_output = subprocess.run(["npm", "install"], cwd=str(web_dir))
                if install_output.returncode != 0:
                    raise RuntimeError(
                        f"Failed to install dependencies for {experience_name}"
                    )

                build_output = subprocess.run(["npm", "run", "build"], cwd=str(web_dir))
                if build_output.returncode != 0:
                    raise RuntimeError(f"Failed to build {experience_name}")

                with open(package_json) as package_json_file:
                    package_json_data = json.load(package_json_file)
                if (
                    (package_json_directories := package_json_data.get("directories"))
                    and isinstance(package_json_directories, dict)
                    and (
                        build_pathname := package_json_directories.get("footron-static")
                    )
                ):
                    static_path = web_dir / build_pathname
                else:
                    static_path = web_dir / "build"
            else:
                static_path = web_dir

            # Make static build directory
            static_build_dir = experience_build_dir / "static"
            static_build_dir.mkdir(parents=True, exist_ok=True)

            # Copy static files to build_dir using subprocess.run
            subprocess.run(["cp", "-r", str(static_path), str(static_build_dir)])




if __name__ == "__main__":
    # Setup argparse
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

    # TODO: Set up diffing so that pull requests do partial builds instead. Should be
    #  fun but a v2 thing for sure.
    # if args.since:
    #     with open(args.since, "rb") as old_experiences_file:
    #         old_experiences = tomli.load(old_experiences_file)
    #     remote_experiences = diff_remote_experiences(
    #         old_experiences, remote_experiences
    #     )

    # TODO: Consider making these into a class once it becomes clear how much state we
    #  need.
    clone_remote_experiences(remote_experiences, experiences_dir)
    build_experiences(experiences_dir, args.path / "build")
