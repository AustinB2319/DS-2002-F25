#!/bin/bash
# refresh_card_sets.sh — Refresh all Pokémon TCG card sets in lookup folder

echo "Refreshing all card sets in card_set_lookup/..."

# Loop through all .json files
for FILE in card_set_lookup/*.json; do
    # If no files exist, skip gracefully
    [ -e "$FILE" ] || { echo "No JSON files found."; exit 0; }

    # Extract the set ID from the filename
    SET_ID=$(basename "$FILE" .json)

    echo "Updating data for set: $SET_ID..."

    # Fetch new data and overwrite existing file
    curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:$SET_ID" -o "$FILE"

    echo "Data written to $FILE"
done

echo "All card sets have been refreshed!"
