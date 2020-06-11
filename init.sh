#!/bin/bash

BASE_DIR="/dbfs/FileStore/tables"
PACKAGE_ARCHIVE_PATH="${BASE_DIR}/wheelhouse/superset_library.tar"
WHEELHOUSE_PATH="${BASE_DIR}/wheelhouse"
PYTHON_REQUIREMENTS_FILE="${BASE_DIR}/python_requirements.txt"
R_REQUIREMENTS_FILE="${BASE_DIR}/R_requirements.txt"
PIP_WHEEL_NAME="pip-20.1-py2.py3-none-any"
PIP_NAME="pip"

PIP_EXECUTABLE=$(which pip3)

# if test -f "$PACKAGE_ARCHIVE_PATH"; then
 #    mkdir -p $WHEELHOUSE_PATH
	# tar -xvf "${PACKAGE_ARCHIVE_PATH}" -C $WHEELHOUSE_PATH
${PIP_NAME} install  "${WHEELHOUSE_PATH}/python/${PIP_WHEEL_NAME}.whl"
for PACKAGE in `cat "$PYTHON_REQUIREMENTS_FILE"`
do
	python3 -m ${PIP_NAME} install --upgrade $PACKAGE --no-index --find-links "${WHEELHOUSE_PATH}/python" || true
done

#rm -rf $WHEELHOUSE_PATH
for filename in `cat "$R_REQUIREMENTS_FILE"`
do
	var="install.packages(\"${WHEELHOUSE_PATH}/R/${filename}\", repos = NULL, type = 'source')"
	Rscript -e "$var" || true
done
# fi
