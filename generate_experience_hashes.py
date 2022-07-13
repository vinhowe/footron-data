from pathlib import Path
from typing import List
import tempfile
import subprocess
from multiprocessing import Pool


def generate_hash_process(experience_path: Path):
    with tempfile.NamedTemporaryFile() as tar_file:
        subprocess.run(
            [
                "tar",
                "cf",
                tar_file.name,
                "--sort=name",
                "--mtime=1970-01-01",
                "--group=root:0",
                "--owner=root:0",
                "-C",
                str(experience_path),
                ".",
            ],
            check=True,
        )
        # Seek to beginning of file
        tar_file.seek(0)
        # Calculate SHA256 hash of tar file
        sha256_hash = (
            subprocess.run(
                ["sha256sum", tar_file.name], stdout=subprocess.PIPE, check=True
            )
            .stdout.split()[0]
            .decode("utf-8")
        )
        # Add hash to dictionary
        return {experience_path.name: sha256_hash}


def generate_experience_hashes(experience_paths: List[Path]):
    hashes = {}
    with Pool(processes=len(experience_paths)) as pool:
        for hash_dict in pool.imap_unordered(generate_hash_process, experience_paths):
            hashes.update(hash_dict)
    return hashes


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "experiences",
        type=Path,
        help="Paths to experiences to hash",
        nargs="+",
    )
    args = parser.parse_args()

    print(generate_experience_hashes(args.experiences))
