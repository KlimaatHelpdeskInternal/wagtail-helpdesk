#!/usr/bin/env bash
# Exit on error
set -o errexit

# install webpack to generate CSS and javascript
npm install --save-dev webpack
# generate CSS and javascript files in Render.  Main.css and main.js will be excluded from GIT
npm run --quiet builddev 
# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r ./requirements/render.txt

# Convert static asset files
#python manage.py collectstatic --no-input

