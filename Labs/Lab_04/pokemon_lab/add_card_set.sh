#!/bin/bash
# add_card_set.sh — Fetch a single Pokémon TCG set and save it as JSON

# Prompt for set ID
read -p "Enter the TCG Card Set ID (e.g., base1, base4): " SET_ID

# Check if user entered something
if [ -z "$SET_ID" ]; then
    echo "Error: Set ID cannot be empty." >&2
    exit 1
fi

# Notify user
echo "Fetching card data for set ID: $SET_ID..."

# Fetch data from Pokémon TCG API and save as JSON
curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:$SET_ID" -o "card_set_lookup/${SET_ID}.json"

# Confirm save
echo "Data saved to card_set_lookup/${SET_ID}.json"
