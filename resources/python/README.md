# CI/CD Python
Continuous Integration/Continuous Development is an environment that is set up to continuously test our software under development. 
These tests run on Gitlab and evaluate whether a build "passes" our criteria. 
Tests include the evaluation of dead code, style analysis, complexity analysis, static type checking, running unit tests and checking for code coverage.
Some of these tests are currently allowed to fail since they require a lot of refactoring before they won't return errors anymore. 
The goal is to have all tests fail a build if it is not up to our coding standard. 

Since we don't want to only find out that a build fails on the Gitlab pipeline, we have some tools in place to run local tests. 
The `build_for_ultimaker.sh` script runs the tests in a docker container with all the required modules.
The separate scripts are also available in the home directory: `run_flake8.sh`, `run_mypy.sh`, `run_dead_code_analysis.sh` etc. in case you are testing a specific part.
These scripts run the scripts in the `ci` directory in a local docker container and use the `references.sh` script as a reference for which files to check. 

By default, all scripts check the local changes, the stages changes and the committed branch changes vs the master branch. 
If you want to have more control on which files to check, you can change the settings to only check the staged and the committed changes. 
In order to do so check the [Only check staged changes section](#only-check-staged-changes).

## Required modules
In order to run the full code style check, be sure to include the following modules to your docker environment:
- pytest
- pytest-cov
- mypy
- vulture
- flake8
- flake8-polyfill
- pytest-mock==1.10.4
- pytest-raises==0.11
- pep8-naming
- flake8-quotes
- flake8-functions

## Only check staged changes
If you want to only compare against staged items and the items on the branch, define `ONLY_CHECK_STAGED` for instance in your ~/.bashrc 
```bash
export ONLY_CHECK_STAGED=1
```
or try out the 2 modes by passing the `ONLY_CHECK_STAGED` to the scripts.
```bash
ONLY_CHECK_STAGED=1 ./build_for_ultimaker.sh
```
or
```bash
ONLY_CHECK_STAGED=1 ./run_flake8.sh
```
etc.

## Check vs different parent branch
In order to check vs a different parent branch, you will need to make 2 changes:
- set the default of PARENT_BRANCH in `references.sh` to your branch for the tests run locally.
- set the PARENT_BRANCH in `.gitlab-ci.yml` to your branch for the tests run in Gitlab. 

## Set up your repo
If you want to add these tools to your repo
- add the ci folder to your root directory
- add the run scripts and `.ini` configurations to your root directory
- add the `.gitlab-ci.yml` configuration to your root directory
- add the `build_for_ultimaker.sh` and `make_docker` scripts to your repo
- be sure to add a `requirements.txt` to your root directory

## IDE integration
The code style checks currently supports Pycharm and VSCode with IDE integration.

### Visual Studio Code
In order to use our preferred Python code style checking tool `Flake8`, we will need to enable this integrated module in the Visual Studio Code [settings](https://code.visualstudio.com/docs/python/linting).
By default, Pylint is enabled as the VSCode linter. 
You can use the command `Python: Select Linter` to disable `Pylint` and to enable `Flake8`. 
Since `Flake8` is integrated in the VSCode IDE, VSCode automatically parses the `.flake8` file as the configuration for the linting, when it is available in the root directory. 

You should now see the Ultimaker specific linting rules take over in the code, and you are ready to get working.

### Pycharm
Pycharm offers no visual inspection integration with `flake8` configurations.
By default, it offers a visual inspection according to the `PEP8` standard.
We want to be able to use the same visual inspection, ignoring the same errors as in the `.flake8` file and using the same code style configurations.
To do this we have added a `.editorconfig` and the `.idea/inspectionProfiles` folder.
The `.editorconfig` file is a file format to define coding styles supported by [many editors](https://editorconfig.org/) and defines the basic coding style.
It includes some Pycharm specific settings to keep a consistent style check over Pycharm IDEs, VSCode does not require this as it parses the `.flake8` file.
The `.idea/inspectionProfiles` folder contains an Ultimaker specific inspection file `UM_inspection.xml` for ignoring UM specific `flake8` errors as defined in the `.flake8` file.
It also contains `profiles_settings.xml` which refers to `UM_inspection.xml` as the default inspection configuration.

You should add the `.editorconfig` to your root directory and move the `inspectionProfiles` to your `.idea/inspectionProfiles` folder. 

You should now see the Ultimaker specific linting rules take over in the code, and you are ready to get working.


