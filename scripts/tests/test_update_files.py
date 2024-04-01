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
    initial_readme_content = """
    # WrongTitle
    Some content in the README file.
    [![Actions Status](https://github.com/latex4ei/WrongCheatsheetTemplate/workflows/CI/badge.svg)](https://github.com/latex4ei/WrongCheatsheetTemplate)
    ## Section
    More details here.
    """.strip()
    fs.create_file(fake_base_path / "README.md", contents=initial_readme_content)
    repo_name = "correct_title"
    github_repository = 'user/correct_title'
    
    updated_content = update_readme_content(initial_readme_content, repo_name, github_repository)
    
    expected_content = """
    # correct_title
    Some content in the README file.
    [![Actions Status](https://github.com/user/correct_title/workflows/CI/badge.svg)](https://github.com/user/correct_title)
    ## Section
    More details here.
    """.strip()
    assert updated_content == expected_content, "README.md content was not updated correctly."

def test_update_cmake_content(fake_base_path, fs):
    initial_cmake_content = """
    cmake_minimum_required(VERSION 3.12)
    project(WrongProjectName NONE)
    # Add the main LaTeX document
    add_latex_document(
        CheatsheetTemplate.tex
        AnotherDoc.tex
        FORCE_PDF
        IMAGE_DIRS img
        DEPENDS writegitid
    )
    """.strip()
    fs.create_file(fake_base_path / "CMakeLists.txt", contents=initial_cmake_content)
    repo_name = "correct_title"

    updated_content = update_cmake_content(initial_cmake_content, repo_name)
    
    expected_content = """
    cmake_minimum_required(VERSION 3.12)
    project(correct_title NONE)
    # Add the main LaTeX document
    add_latex_document(
        correct_title.tex
        AnotherDoc.tex
        FORCE_PDF
        IMAGE_DIRS img
        DEPENDS writegitid
    )
    """.strip()
    assert updated_content == expected_content, "CMakeLists.txt content was not updated correctly."
