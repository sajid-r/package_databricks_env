import pkg_resources
import sys, os
import argparse

TAR_NAME = 'superset_library.tar'
ERROR_LOG = 'error.log'
R_SCRIPT_NAME = 'build_packages.R'
PIP_VERSION = '20.1'
PIP_NAME = 'pip3'
PYTHON_VERSION = '3.6'
BASE_DIR = '/dbfs/FileStore/tables'
PYTHON_NAME = 'python3'

def R_main(destination, requirements, error_file):
    RDestination = f"{destination}/R"
    if not os.path.exists(RDestination):
        os.makedirs(RDestination)

    #download environment packages
    script_path = os.path.join(BASE_DIR, R_SCRIPT_NAME)
    os.system(f"Rscript --vanilla {script_path} >> {os.path.join(BASE_DIR, 'R_log.log')}")

    #include custom packages in the folder.
    print("Copying custom packages.")
    for item in os.listdir('.'):
        if item[-3:] == 'tar' or item[-6:] == 'tar.gz':
            exitCode = os.system(f'cp {item} {RDestination}/{item}')
            #exitCode == 0 for successfull downloads
            if exitCode:
                os.system(f"echo {item} >> {error_file}")
            else:
                os.system(f"echo {item} >> {logDestination}")



def python_main(destination, requirements, error_file, sanity_flag=False):
    
    # create a package log file
    logDestination = os.path.join(BASE_DIR, "python_log.log")

    #remove previous logs if exist
    try:
        os.remove(logDestination)
    except OSError:
        pass

    try:
        os.remove(error_file)
    except OSError:
        pass

    #create Python folder if not exists
    pythonDestination = f"{destination}/python"
    if not os.path.exists(pythonDestination):
        os.makedirs(pythonDestination)

    installed_packages = {d.project_name: d.version for d in pkg_resources.working_set}

    #install pip3
    os.system("sudo apt-get -y install python3-pip")
    os.system(f"{PIP_NAME} install --upgrade pip")
    os.system(f"{PYTHON_NAME} -m pip install --upgrade pip")

    # for all installed packages in the Databricks environment, download the wheel file for exact version
    if not sanity_flag:
        print("Downloading environment packages...")
        for package, version in list(installed_packages.items()):
            print(f"{PIP_NAME} download {package}=={version}    -d {pythonDestination} --platform=manylinux1_x86_64 --only-binary=:all: --python-version {PYTHON_VERSION}")
            exitCode = os.system(f"{PIP_NAME} download {package}=={version} -d {pythonDestination} --platform=manylinux1_x86_64 --only-binary=:all: --python-version {PYTHON_VERSION}")

            #exitCode == 0 for successfull downloads
            if exitCode:
                print(f"{PIP_NAME} download {package}=={version} -d {pythonDestination}")
                exitCode = os.system(f"{PIP_NAME} download {package}=={version} -d {pythonDestination}")
                if exitCode:
                    print(f"{PYTHON_NAME} -m pip download {package}=={version} -d {pythonDestination}")
                    exitCode = os.system(f"{PYTHON_NAME} -m pip download {package}=={version} -d {pythonDestination}")
                    if exitCode:
                        print(f"{PIP_NAME} download {package} -d {pythonDestination}")
                        exitCode = os.system(f"{PIP_NAME} download {package} -d {pythonDestination}")
                        if exitCode:
                            os.system(f"echo {package}=={version} >> {error_file}")
                        else:
                            os.system(f"echo {package} >> {logDestination}")
                    else:
                        os.system(f"echo {package}=={version} >> {logDestination}")
                else:
                    os.system(f"echo {package}=={version} >> {logDestination}")
            else:
                os.system(f"echo {package}=={version} >> {logDestination}")


    #For addtional requirements or specific version requests that need to be included in the superset
    if requirements:
        print("Downloading packages from the requirements file...")
        with open(requirements, 'r') as csv:
            for line in csv.readlines():
                package, version = line.split('==')
                if version:
                    print(f"{PIP_NAME} download {package}=={version} -d {pythonDestination} --platform=manylinux1_x86_64 --only-binary=:all: --python-version {PYTHON_VERSION}")
                    exitCode = os.system(f"{PIP_NAME} download {package}=={version} -d {pythonDestination} --platform=manylinux1_x86_64 --only-binary=:all:")
                    
                    #exitCode == 0 for successfull downloads
                    if exitCode:
                        print(f"{PIP_NAME} download {package}=={version} -d {pythonDestination}")
                        exitCode = os.system(f"{PIP_NAME} download {package}=={version} -d {pythonDestination}")
                        if exitCode:
                            print(f"{PYTHON_NAME} -m pip download {package}=={version} -d {pythonDestination}")
                            exitCode = os.system(f"{PYTHON_NAME} -m pip download {package}=={version} -d {pythonDestination}")
                            if exitCode:
                                print(f"{PIP_NAME} download {package} -d {pythonDestination}")
                                exitCode = os.system(f"{PIP_NAME} download {package} -d {pythonDestination}")
                                if exitCode:
                                    os.system(f"echo {package}=={version} >> {error_file}")
                                else:
                                    os.system(f"echo {package} >> {logDestination}")
                            else:
                                os.system(f"echo {package}=={version} >> {logDestination}")
                        else:
                            os.system(f"echo {package}=={version} >> {logDestination}")
                    else:
                        os.system(f"echo {package}=={version} >> {logDestination}")

                else:
                    print(f"{PIP_NAME} download {package} -d {pythonDestination} --platform=manylinux1_x86_64 --only-binary=:all: --python-version {PYTHON_VERSION}")
                    exitCode = os.system(f"{PIP_NAME} download {package} -d {pythonDestination} --platform=manylinux1_x86_64 --only-binary=:all: --python-version {PYTHON_VERSION}")

                    #exitCode == 0 for successfull downloads
                    if exitCode:
                        print(f"{PIP_NAME} download {package} -d {pythonDestination}")
                        exitCode = os.system(f"{PIP_NAME} download {package} -d {pythonDestination}")
                        if exitCode:
                            os.system(f"echo {package} >> {error_file}")
                        else:
                            os.system(f"echo {package} >> {logDestination}")
                    else:
                        os.system(f"echo {package} >> {logDestination}")

    #include custom packages in the folder.
    print("Copying custom packages.")
    for item in os.listdir('.'):
        if item[-3:] == 'whl':
            exitCode = os.system(f'cp {item} {pythonDestination}/{item}')
            #exitCode == 0 for successfull downloads
            if exitCode:
                os.system(f"echo {item} >> {error_file}")
            else:
                os.system(f"echo {item} >> {logDestination}")


    #include custom packages in the folder.
    print("Copying additional packages.")
    exitCode = os.system(f"{PIP_NAME} download pip=={PIP_VERSION} -d {pythonDestination} --platform=manylinux1_x86_64 --only-binary=:all:")
    #exitCode == 0 for successfull downloads
    if exitCode:
        os.system(f"echo {item} >> {error_file}")
    else:
        os.system(f"echo {item} >> {logDestination}")


    #create a requirements file
    reqDestination = os.path.join(destination, "package_list.txt")
    os.system(f"pip freeze > {reqDestination}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Packaging environment dependencies into a superset tar.')

    parser.add_argument('--destination',
                        type=str,
                        help='Path to the folder where all the wheels should be stored. The final tar file is also stored in this folder.')

    known_args, pipeline_args = parser.parse_known_args()
    
    parser.add_argument('--requirements',
                        type=str,
                        default=None,
                        help='Path to the requirements file with additional packages or package versions that need to be downloaded and included in the superset tar.')

    parser.add_argument('--error',
                        type=str,
                        default=ERROR_LOG,
                        help='Path to the error log file.')

    parser.add_argument('-R', action='store_true')

    parser.add_argument('-python', action='store_true')

    parser.add_argument('-sanity_check', action='store_false')

    known_args, pipeline_args = parser.parse_known_args()

    #run sanity_check mode
    if known_args.sanity_check:
        python_main(known_args.destination, known_args.requirements, known_args.error, sanity_flag=True)
        os.system(f"cd {known_args.destination} && tar cvf {TAR_NAME} *")
        return

    #create destination folder if not exists.
    if not os.path.exists(known_args.destination):
        os.makedirs(known_args.destination)

    if (known_args.python):
        print("Downloading Python packages...")
        python_main(known_args.destination, known_args.requirements, known_args.error)
    if (known_args.R):
        print("Downloading R packages...")
        R_main(known_args.destination, known_args.requirements, known_args.error)

    #tar and save to location
    print(f"Download Completed. Compressing into {TAR_NAME}")
    #remove previous tar if exists
    try:
        path = os.path.join(known_args.destination, TAR_NAME)
        os.remove(path)
    except OSError:
        pass

    os.system(f"cd {known_args.destination} && tar cvf {TAR_NAME} *")