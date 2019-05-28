# Introduction

This document will give an overview of the current CI setup for the Ultimaker Platform team.

# Table of contents

<!-- MarkdownTOC autolink="true" bracket="round" levels="1,2,3,4" markdown_preview="markdown" -->

- [Software and services](#software-and-services)
- [Gitlab Runner \(Dave\)](#gitlab-runner-dave)
- [Gitlab CI](#gitlab-ci)
  - [.gitlab-ci.yml](#gitlab-ciyml)
    - [What is yaml?](#what-is-yaml)
      - [Pointers](#pointers)
      - [Hidden sections](#hidden-sections)
      - [Common parameters](#common-parameters)
    - [Gitlab `.yml` configuration](#gitlab-yml-configuration)
      - [Variables that configure `git`](#variables-that-configure-git)
      - [Environment variables available in a job](#environment-variables-available-in-a-job)
    - [Stages](#stages)
  - [Gitlab CI web configuration](#gitlab-ci-web-configuration)
  - [Pipeline triggers](#pipeline-triggers)
    - [Passing variables between jobs](#passing-variables-between-jobs)
- [Included projects](#included-projects)
- [Access](#access)
- [CI Dashboard](#ci-dashboard)
- [Known issues](#known-issues)

<!-- /MarkdownTOC -->

# Software and services
We use the following in our CI efforts:

- **[Github](https://github.com/Ultimaker/):** To and from where we normally push and pull code. Since development happens on Github, repositories with CI support are periodically cloned from Github to Gitlab.
- **[Gitlab CI](https://docs.gitlab.com/ee/ci/README.html):** Gitlab is a code repository like Github, with the ability to run pipelines to test and package our code. Gitlab periodically pulls all repositories from Github, so regular commits should be made to Github.
- **[Gitlab Runner](https://docs.gitlab.com/runner/):** The software behind Gitlab that runs said pipelines. It exists in cloud form and in local form. We'd like to move to the cloud-hosted version, but since we need access to parts of the host that are not available on cloud-hosted runners, we're stuck with our own local Runner; Dave.
- **[Docker](https://docs.docker.com/install/):** We use Docker to reliably set up a build environment for each or our projects. Images can be stores in a Gitlab-specific image repository. See the [prepare](#prepare) stage below for the logic behind image building.
- **[PlatformIO](https://docs.platformio.org/en/latest/):** A service that can run test on real hardware in the CI process. PlatformIO integrates easily with Gitlab, you can find an example [here](https://docs.platformio.org/en/latest/ci/gitlab.html).

# Gitlab Runner (Dave)
Our runner, affectionately called Dave, is currently mostly a black box. Although it still does it's job well, the password to access it is currently unknown.

A ticket has been made to rebuild Dave, after that's complete, documentation on how to setup Dave will be added here.

# Gitlab CI
Gitlab CI setup is done using a `.gitlab-ci.yml` file in the root of your repository, as well as through the Gitlab website.

## .gitlab-ci.yml
`.gitlab-ci.yml` is a special file in the root of your repository that configures Gitlab CI. You can find the `.gitlab-ci.yml` reference [here](https://docs.gitlab.com/ee/ci/yaml/).

### What is yaml?
Yaml is a markup language designed to be easily readable. If you are new to yaml, have a look [here](https://learnxinyminutes.com/docs/yaml/)

#### Pointers
Pay special attention to pointers and how to merge them into lists using the `<<` operator. They insert the corresponding code suffixed with `&name`. We use this extensively to avoid rehashing code.

#### Hidden sections
Sections in the `.yml` file starting with a `.` are not visible to Gitlab, but can be used for storing parameters which can be merged into visible sections later on.

#### Common parameters
Most sections in our `.yml` files will start with a `<< common_ ...` line. Here we use pointers and hidden sections to avoid repeating code.

### Gitlab `.yml` configuration
Gitlab supports settings various variables for advanced configuration.

#### Variables that configure `git`
[`GIT_SUBMODULE_STRATEGY: recursive`](https://docs.gitlab.com/ee/ci/git_submodules.html#using-git-submodules-in-your-ci-jobs) is set to make Gitlab automatically clone submodules when cloning the source.

[`GIT_DEPTH: 1`](https://docs.gitlab.com/ee/ci/large_repositories/#shallow-cloning) is set for some repositories to speed up `git clone` by doing a shallow clone. This is especially useful for um-kernel as cloning the Linux kernel with this setting saves a huge amount of time.

#### Environment variables available in a job
We use some [Gitlab predefined variables](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html) in our `.yml` files.

### Stages
We've divided up our pipelines in the following stages.

  - **lint:** Runs several linting scripts in parallel.
  - **prepare:** Builds a Docker environment for the build. We try to skip this stage if there are no changes to the Dockerfile.
  - **push:** Runs only when we prepared a new Docker environment, if this environment was created successfully, and if we're on the master branch. This stage uploads the docker image we just created to the local Gitlab Docker image repository so it can be reused in subsequent builds.
  - **build:** Runs the actual build script. Gitlab keeps the artifacts and puts them up for download.
      + **Old setup:**
          * build:dev_docker_candidate
          * build:dev_docker_latest
          * build:master_docker_latest  
      + **New setup:**
          * build:branch
          * build:master
  - **test:** Runs tests on the built artifact. Not yet available for all repositories.
  - **cleanup:** Mainly intended to keep track of Docker images; which ones to keep and which ones to throw away.

## Gitlab CI web configuration
Pipelines are configured using a `.gitlab-ci.yml` file for each project. However, the Gitlab's web-interface also provides several configuration options.

Note that not all settings are available if you don't have the proper access rights on Gitlab! If you can't find something listed here, ask a supervisor to bump your rights.

Notable settings are:

  - **Settings > Repository > Default Branch:** Generally speaking this should be `master`, unless you are setting up CI for a new project. Gitlab only enables CI features for a repository when there is a `.gitlab-ci.yml` file in the root of the Default Branch.
  - **Settings > CI / CD > Runners:** Since our projects need "[Dave](#gitlab-runner-dave)"'s custom setup to run, be sure to click _"Disable shared Runners"_ so jobs aren't run on Gitlab's shared runners where they will fail.
  - **Settings > CI / CD > Variables:** A place to put secret variables that you can access in the environment. Gitlab _should_ hide them from the logs, but that feature is pretty patchy...
  - **Settings > CI / CD > Pipeline Triggers:** Tokens that can be used to trigger other pipelines. Must be created on the _triggered_ pipeline. See [triggers](#triggers) for a more detailed explanation.

## Pipeline triggers
Triggers offer the possibility of starting a pipeline from a script. In our case we use them to trigger an image build whenever something changes upstream.

Packages that produce a .deb file will trigger a pipeline for the jedi-build repository that will output an image which includes that .deb.

We haven't decided on where to store these artifacts yet. Currently we grab the artifacts that were produced by Gitlab, send them to an `override` folder and include them in the image. A demo of this functionality can be found in `um-kernel`.

In the future, we might automatically commit all packages produced on the projects' master branches into `jedi-package-repository`, making it easier to produce an image with all the latest packages inside.

What is included in your image produced by a trigger?

**If you commit to `master`**, the script will take all the latest versions of all packages from their master branches, to give you an image with all the latest code. This image will appear as an artifact on the `master` branch of `jedi-build`.

**If you commit to your own branch**, the script will _not_ build an image by default. If you'd like automated image creation for your branch, create an identically-named branch on jedi-build. The script will then take all the latest versions of all packages from their master branches, _except_ for projects where a branch exists with the same name.

### Passing variables between jobs

# Included projects

Project             | CI Status   | Notes
--------------------|-------------|------------------
Air Manager         | Working     | Uses PlatformIO to run tests on real hardware.
jedi-system-update  | Partial     | No triggers to build an image.
Opinicus            | Partial     | Pipeline does not produce a `.deb` file yet.
um-kernel           | Working     |

# Access
Gitlab access is granted on a need-to-use basis. Note that not all settings are available without the proper access rights, and that you might not be able to download the artifacts or logs that you're looking for. To mitigate this issue, we created the [Ultimaker CI Dashboard](ci-dashboard), which should give access to everything you _should_ need.

If you need more access, ask a supervisor to grant it to you.

# CI Dashboard
The [Ultimaker CI Dashboard](https://github.com/Ultimaker/ci-dashboard) is a web-interface designed to give you a quick overview of, and access to things you need from Gitlab as a developer, without the need to log in. Currently you need clone it, supply it with an access token and run it locally, but in the near future we will make it accessible for everyone on the internal network.

# Known issues
Below is a list of known issues, some of which we're still working on.

- [Gitlab keeps branches that were deleted from Github.](https://gitlab.com/gitlab-org/gitlab-ee/issues/1344)
- Dave is currently a black box

