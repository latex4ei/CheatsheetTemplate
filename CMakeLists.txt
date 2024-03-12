cmake_minimum_required(VERSION 3.12)

project(CheatsheetTemplate NONE)
include(UseLATEX)

add_custom_target(
    writegitid ALL
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/write-gitid.sh
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
)

add_latex_document(
    CheatsheetTemplate.tex
    FORCE_PDF
    IMAGE_DIRS img
    DEPENDS writegitid
)
