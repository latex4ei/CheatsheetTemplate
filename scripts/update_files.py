from pathlib import Path
import re
import os
import sys

def check_tex_file_exists(repo_name: str, base_path: Path):
    """Check if a .tex file with the same name as the repository exists."""
    tex_file_path = base_path / f"{repo_name}.tex"
    if not tex_file_path.exists():
        msg = f"No .tex file found with the name {tex_file_path.name}. File name must match repo name."
        raise FileNotFoundError(msg)

def update_readme_content(content: str, repo_name: str, github_repository: str) -> str:
    """Updates the README.md content."""
    # Update the first line with the repository name
    content = re.sub(r'^.*', f'# {repo_name}', content, count=1)
    # Update the GitHub Actions status badge
    actions_status_line = f'[![Actions Status](https://github.com/{github_repository}/workflows/CI/badge.svg)](https://github.com/{github_repository})'
    return re.sub(r'\[!\[Actions Status\].*', actions_status_line, content)

def update_cmake_content(content: str, repo_name: str) -> str:
    """Updates the CMakeLists.txt content."""
    content = re.sub(r'project\(([^ ]*)', f'project({repo_name}', content, count=1)
    return re.sub(r'([^ ]*\.tex)', f'{repo_name}.tex', content, count=1)

def main(github_repository: str):
    repo_name = Path(github_repository).name
    base_path = Path(__file__).parent.parent

    check_tex_file_exists(repo_name, base_path)
    
    readme_path = base_path / 'README.md'
    cmake_path = base_path / 'CMakeLists.txt'
    
    # Read and update README.md content
    readme_content = readme_path.read_text()
    updated_readme_content = update_readme_content(readme_content, repo_name, github_repository)
    readme_path.write_text(updated_readme_content)
    
    # Read and update CMakeLists.txt content
    cmake_content = cmake_path.read_text()
    updated_cmake_content = update_cmake_content(cmake_content, repo_name)
    cmake_path.write_text(updated_cmake_content)

if __name__ == "__main__":
    main(os.getenv('GITHUB_REPOSITORY'))
