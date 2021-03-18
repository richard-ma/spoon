#!/bin/bash

function echo_help() {
  echo "Usage: "
  echo "  ./project-update.sh [project-name]"
}

function msg() {
  echo "***[$1]***"
}

project_name="$1"

if [ "" = "$project_name" ]; then
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
  pip install -r requirements.txt
fi
msg "PIP Install Completed"

# scrapyd-deploy
cd "$project_name"
msg "Changing To $project_name Folder"
msg "Deploying Project"
scrapyd-deploy
msg "Deployed Project"