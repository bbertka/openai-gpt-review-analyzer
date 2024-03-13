#!/bin/bash

# Read the list of items from the file
while IFS= read -r item; do
  # URL encode the item (requires `jq` utility)
  encoded_item=$(jq -nr --arg item "$item" '$item|@uri')
  
  # Execute the curl command
  curl "http://192.168.1.110:5000/sentiment?item=${encoded_item}"
done < ./items1.txt
