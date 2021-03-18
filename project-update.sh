#!/bin/bash

function echo_help() {
  echo "Usage: "
  echo "  ./project-update.sh [project-name] [scrapyd_folder]"
}

function msg() {
  echo "***[$1]***"
}

project_name="$1"
scrapyd_folder="$2"

if [ "" = "$project_name" ] || [ "" = "$scrapyd_folder" ]; then
  echo_help
  exit 1
fi

# git pull
msg "Git Pull"
git pull origin main --depth=1
git log -2
msg "Git Pull Completed"

# checking venv
if [ -d "venv" ]; then
  source venv/bin/activate
  msg "Start venv"
else
  virtualenv -p python3 venv
  msg "Created venv"
  source venv/bin/activate
  msg "Start venv"
fi

# update requiements.txt
msg "PIP Install"
if [ -f "requirements.txt" ]; then
  pip3 install -r requirements.txt
fi
msg "PIP Install Completed"

# scrapyd-deploy
cd "$project_name"
msg "Changing To $project_name Folder"
msg "Deploying Project"
scrapyd-deploy
msg "Deployed Project"

# deactivate venv
deactivate
msg "Deactivate $project_name venv"

# update scrapyd env
source "$scrapyd_folder"/bin/activate
msg "Start scrapyd venv"
msg "PIP Install"
if [ -f "requirements.txt" ]; then
  pip3 install -r requirements.txt
fi
msg "PIP Install Completed"
deactivate
msg "Deactivate $scrapyd_folder venv"
