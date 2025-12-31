import re
import sys
from pathlib import Path

def bump_version(file_path: str, part: str = 'patch'):
    path = Path(file_path)
    content = path.read_text()
    
    # Regex to find version = "x.y.z"
    pattern = r'version = "(\d+)\.(\d+)\.(\d+)"'
    match = re.search(pattern, content)
    
    if not match:
        print(f"Error: version not found in {file_path}")
        sys.exit(1)
        
    major, minor, patch = map(int, match.groups())
    
    if part == 'major':
        major += 1
        minor = 0
        patch = 0
    elif part == 'minor':
        minor += 1
        patch = 0
    else: # patch
        patch += 1
        
    new_version = f"{major}.{minor}.{patch}"
    new_content = re.sub(pattern, f'version = "{new_version}"', content)
    
    path.write_text(new_content)
    print(f"Bumped version to {new_version}")

if __name__ == "__main__":
    # Default to bumping patch
    part = sys.argv[1] if len(sys.argv) > 1 else 'patch'
    bump_version("pyproject.toml", part)
