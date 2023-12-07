# GET STARTED
## Requirement
* **WSL**
* **Python 3.11+**
* **Docker**

## Build the project
1) `Enter WSL (Windows ONLY)`
    * Open terminal -> type `WSL` -> Hit Enter -> type `cd` -> Hit Enter
2) `git clone git@github.com:Knox-AAU/Preprocessessing_Text-extraction.git`
3) `cd Preprocessessing_Text-extraction`
4) `source run setup`

## Easy shell commands (Custom script)

***How to start dev environment***
```bash
sh run dev up
```

***How to stop dev environment***
```bash
sh run dev down
```

***How to lint project***
```bash
sh run lint
```

***How to run project tests***
```bash
sh run test
```

***How to run prod environment (SERVER ONLY)***
```bash
sh run prod up
```

***How to stop prod environment (SERVER ONLY)***
```bash
sh run prod down
```

## How to contribute
To be able to contribute to this project you will need fulfill following requirements:
* **Branching**
    * *To begin your contribution you've to branch out directly from main. Remember to pull the newest version before branching out. When you're done with the branch, you create a pull request and get it approved by another person working on the project.*
    * To make a new branch directly from terminal, you can use following commands:
    * ``git pull``
    * ``git checkout -b {branchName}`` (e.g. **git checkout -b jc/new-branch-name**)
    * ``git add {files}``
    * ``git commit -m {comment about changes}``
    * ``git push origin {branchName}`` (e.g. **git push origin jc/new-branch-name**)
* **Pull_requests**
    * Atleast one person is required to review changes
    * When pull_request is created, the workflow starts running - Checking for code structure, using a linter, and checking if unittests and other tests passes
        * If workflow fails, then merging is blocked until fixed
* **Workflow**
    * Workflow is built through 3 steps, where last step is divided in 3 parts
        * Linter - Ensure good structure and readable code
        * Unittest - Build-in testing module, ensuring integrity and validation of modules
        * Deployment - Creates production packages that is pulled on server. Deployment creates three packages, one for each step in text-extraction. To run deployment, production branch (Main) need to be tagged, before workflow constructs packages.

## Deployment
* **How to tag production**
    * To tag the new production it can be done through terminal
        * ``git tag {version} {branchName}`` (e.g. **git tag 1.2 main**)
* **How to deploy new version**
    * After tagging next production package it is possible to pull from server
    * Connect to AAU VPN
    * Ssh into preproc01 `ssh <STUDENT_MAIL>@knox-preproc01.srv.aau.dk`
    * Two options:
        * Git clone project and use `sh run prod up`
        * ``sudo docker compose -f docker-compose-prod.yml pull`` && ``docker compose -f docker-compose-prod.yml up``
    * Watchtower will pull new versions in future

---
---
---
---
---

# Advanced/Detailed commands for project
## Activating and setting up virtualenv
```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

## To lint code
1) Be in folder with files you want to lint (usually root)
2) 
```bash
pylint ./**/*.py
```

## To run tests
1) Be in root folder 
2) 
```bash
python -m unittest discover -s src -p 'test_*.py'
```

## Command to setup setuptools and fix imports etc
```bash
python -m pip install --editable .
```

## Docker compose commands
*Sudo rights may be needed - use: " **sudo {command you want to run}** "*
#### Build containers
* **To build developer environment**
```bash
docker compose -f docker-compose-dev.yml build
```
* **To pull production environment**
```bash
docker compose -f docker-compose-prod.yml pull
```

#### Start containers
* **To run developer environment**
```bash
docker compose -f docker-compose-dev.yml up -d
```
* **To run production environment**
```bash
docker compose -f docker-compose-prod.yml up -d
```

#### Stop containers
* **To stop developer environment**
```bash
docker compose -f docker-compose-dev.yml down
```
* **To stop production environment**
```bash
docker compose -f docker-compose-prod.yml down
```