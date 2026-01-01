import re
import sys
from pathlib import Path


def bump_version(file_path: str, argument: str = "patch"):
    path = Path(file_path)
    content = path.read_text()

    # Regex to find version = "x.y.z"
    pattern = r'version = "(\d+)\.(\d+)\.(\d+)"'
    match = re.search(pattern, content)

    if not match:
        print(f"Error: version not found in {file_path}")
        sys.exit(1)

    # Check if argument is a specific version (X.Y.Z)
    if re.match(r"^\d+\.\d+\.\d+$", argument):
        new_version = argument
    else:
        major, minor, patch = map(int, match.groups())

        if argument == "major":
            major += 1
            minor = 0
            patch = 0
        elif argument == "minor":
            minor += 1
            patch = 0
        elif argument == "patch":
            patch += 1
        else:
            print(f"Error: Invalid argument '{argument}'. Must be 'major', 'minor', 'patch', or a specific version like '1.2.3'.")
            sys.exit(1)

        new_version = f"{major}.{minor}.{patch}"

    new_content = re.sub(pattern, f'version = "{new_version}"', content)

    path.write_text(new_content)
    print(f"Bumped version to {new_version}")


if __name__ == "__main__":
    # Default to bumping patch
    argument = sys.argv[1] if len(sys.argv) > 1 else "patch"
    # Strip 'v' prefix if present (e.g., v0.2.3 -> 0.2.3)
    if argument.startswith("v"):
        argument = argument[1:]
    
    bump_version("pyproject.toml", argument)
