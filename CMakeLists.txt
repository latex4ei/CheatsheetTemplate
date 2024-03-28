cmake_minimum_required(VERSION 3.12)

project(CheatsheetTemplateNot NONE)
include(UseLATEX)

add_custom_target(
    writegitid ALL
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/write-gitid.sh
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
)

set(IMAGE_DIRS
    img
    # Add subdirectories here
    # img/logic
    # img/rca
)

add_latex_document(
    CheatsheetTemplateNotNot.tex
    FORCE_PDF
    IMAGE_DIRS ${IMAGE_DIRS}
    DEPENDS writegitid
)
