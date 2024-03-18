# Read the list of items from the file and execute the curl command concurrently
cat items2.txt | while IFS= read -r item; do
  # URL encode the item (requires `jq` utility)
  encoded_item=$(jq -nr --arg item "$item" '$item|@uri')
  
  # Execute the curl command
  curl "http://192.168.1.110:5000/sentiment?item=${encoded_item}" &
done

# Wait for all background jobs to complete
wait

echo "All jobs completed."
