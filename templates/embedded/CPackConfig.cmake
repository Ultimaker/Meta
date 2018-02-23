# Debian package
set(CPACK_GENERATOR "DEB")
set(CPACK_DEBIAN_PACKAGE_SUGGESTS "opinicus")
set(CPACK_DEBIAN_PACKAGE_SECTION "net")

set(CPACK_DEBIAN_PACKAGE_ARCHITECTURE all)

# NOTE!! 1) do not copy this note into your repo, 2) this are just example
# dependencies. linux-base is the kernel base package, python3 may not be
# needed for your project!
set(CPACK_DEBIAN_PACKAGE_DEPENDS
    "linux-base (>= 3.2),
     python3 (>= 3.4)"
)

set(CPACK_DEBIAN_PACKAGE_CONTROL_EXTRA "${CMAKE_CURRENT_SOURCE_DIR}/debian/preinst;${CMAKE_CURRENT_SOURCE_DIR}/debian/postinst;${CMAKE_CURRENT_SOURCE_DIR}/debian/prerm;")

set(CPACK_PACKAGE_FILE_NAME "${PROJECT_NAME}-${CPACK_PACKAGE_VERSION}_${CPACK_DEBIAN_PACKAGE_ARCHITECTURE}")
