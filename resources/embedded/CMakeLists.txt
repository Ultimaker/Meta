cmake_minimum_required(VERSION 3.4.3)
project(dummy_template_project)

include(GNUInstallDirs)

find_package(Git)
set(GIT_VERSION "Unknown")
if(GIT_FOUND)
    message("git found: ${GIT_EXECUTABLE} (ver: ${GIT_VERSION_STRING})")
    execute_process(COMMAND ${GIT_EXECUTABLE} describe --dirty --tags --always OUTPUT_VARIABLE GIT_VERSION OUTPUT_STRIP_TRAILING_WHITESPACE)
endif()

install(
    FILES "${CMAKE_SOURCE_DIR}/LICENSE"
    DESTINATION "${CMAKE_INSTALL_FULL_DOCDIR}"
)

if(EXISTS "${CMAKE_ROOT}/Modules/CPack.cmake")
    set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Ultimaker dummy template (${GIT_VERSION})")
    set(CPACK_PACKAGE_VENDOR "Ultimaker")
    set(CPACK_PACKAGE_CONTACT "Ultimaker <info@ultimaker.com>")
    if(NOT DEFINED CPACK_PACKAGE_VERSION)
        set(CPACK_PACKAGE_VERSION "9999.99.99.${GIT_VERSION}")
    endif()
    include(CPackConfig.cmake)
    include(CPack)
endif()
