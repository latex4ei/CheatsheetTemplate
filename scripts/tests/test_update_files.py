import pytest
from scripts.update_files import check_tex_file_exists, update_readme_content, update_cmake_content
from pathlib import Path
import os

@pytest.fixture
def fake_base_path(fs):
    """Fixture to create a base path and mock environment variable."""
    base_path = Path("/test/project")
    fs.create_dir(base_path)
    os.environ['GITHUB_REPOSITORY'] = 'user/correct_title'
    return base_path

def test_check_tex_file_exists__file_does_not_exist__should_raise(fake_base_path, fs):
    repo_name = "correct_title"
    fs.create_file(fake_base_path / f"{repo_name}.tex")
    check_tex_file_exists(repo_name, fake_base_path)
    
    with pytest.raises(FileNotFoundError):
        check_tex_file_exists("nonexistent_repo", Path(fake_base_path))

def test_update_readme_content(fake_base_path, fs):
    initial_readme_content = (
        "# WrongTitle\n"
        "Some content in the README file.\n"
        "[![Actions Status](https://github.com/latex4ei/WrongCheatsheetTemplate/workflows/CI/badge.svg)](https://github.com/latex4ei/WrongCheatsheetTemplate)\n"
        "## Section\n"
        "More details here."
    )
    fs.create_file(fake_base_path / "README.md", contents=initial_readme_content)
    repo_name = "correct_title"
    github_repository = 'user/correct_title'
    
    updated_content = update_readme_content(initial_readme_content, repo_name, github_repository)
    
    expected_content = (
        "# correct_title\n"
        "Some content in the README file.\n"
        "[![Actions Status](https://github.com/user/correct_title/workflows/CI/badge.svg)](https://github.com/user/correct_title)\n"
        "## Section\n"
        "More details here."
    )
    assert updated_content == expected_content, "README.md content was not updated correctly."

def test_update_cmake_content(fake_base_path, fs):
    initial_cmake_content = (
        "cmake_minimum_required(VERSION 3.12)\n"
        "project(WrongProjectName NONE)\n"
        "# Add the main LaTeX document\n"
        "add_latex_document(\n"
        "CheatsheetTemplate.tex\n"
        "AnotherDoc.tex\n"
        "FORCE_PDF\n"
        "IMAGE_DIRS img\n"
        "DEPENDS writegitid\n"
        ")\n"
    )
    fs.create_file(fake_base_path / "CMakeLists.txt", contents=initial_cmake_content)
    repo_name = "correct_title"

    updated_content = update_cmake_content(initial_cmake_content, repo_name)
    
    expected_content = (
        "cmake_minimum_required(VERSION 3.12)\n"
        "project(correct_title NONE)\n"
        "# Add the main LaTeX document\n"
        "add_latex_document(\n"
        "correct_title.tex\n"
        "AnotherDoc.tex\n"
        "FORCE_PDF\n"
        "IMAGE_DIRS img\n"
        "DEPENDS writegitid\n"
        ")\n"
    )
    assert updated_content == expected_content, "CMakeLists.txt content was not updated correctly."
