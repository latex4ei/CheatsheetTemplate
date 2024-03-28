from pathlib import Path
import re
import os
import sys

def check_tex_file_exists(repo_name: str, base_path: Path):
    """Check if a .tex file with the same name as the repository exists."""
    tex_file_path = base_path / f'{repo_name}.tex'
    if not tex_file_path.exists():
        sys.exit(f"Error: No .tex file found with the name {repo_name}.tex")

def read_file(file_path: Path) -> str:
    """Reads the entire content of a file and returns it as a string."""
    return file_path.read_text()

def write_file(file_path: Path, content: str):
    """Writes the given content to a file, replacing its previous content."""
    file_path.write_text(content)

def update_readme_content(content: str, repo_name: str) -> str:
    """Updates the README.md content."""
    content = re.sub(r'^.*', f'# {repo_name}', content, count=1)
    actions_status_line = f'[![Actions Status](https://github.com/{os.getenv("GITHUB_REPOSITORY")}/workflows/CI/badge.svg)](https://github.com/{os.getenv("GITHUB_REPOSITORY")})'
    return re.sub(r'\[!\[Actions Status\].*', actions_status_line, content)

def update_cmake_content(content: str, repo_name: str) -> str:
    """Updates the CMakeLists.txt content."""
    content = re.sub(r'project\(([^ ]*)', f'project({repo_name}', content, count=1)
    return re.sub(r'([^ ]*\.tex)', f'{repo_name}.tex', content, count=1)

def main():
    repo_name = os.getenv('GITHUB_REPOSITORY').split('/')[-1]
    base_path = Path(__file__).parent

    check_tex_file_exists(repo_name, base_path)
    
    readme_path = base_path / 'README.md'
    cmake_path = base_path / 'CMakeLists.txt'
    
    readme_content = read_file(readme_path)
    updated_readme_content = update_readme_content(readme_content, repo_name)
    write_file(readme_path, updated_readme_content)
    
    cmake_content = read_file(cmake_path)
    updated_cmake_content = update_cmake_content(cmake_content, repo_name)
    write_file(cmake_path, updated_cmake_content)

if __name__ == "__main__":
    main()
