#!/bin/bash

# Fetch all branches from origin (GitLab in this setup)
git fetch origin

# Loop through all local branches
for branch in $(git for-each-ref --format='%(refname:short)' refs/heads/); do
  echo "Processing $branch..."
  
  # Checkout the branch
  git checkout "$branch"
  
  # Pull latest changes from GitLab (origin)
  git pull origin "$branch"
  
  # Push the branch to GitHub
  git push github "$branch"
done

# Optionally, switch back to the main branch at the end
git checkout main
