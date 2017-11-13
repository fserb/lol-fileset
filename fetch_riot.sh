#!/bin/bash

API_KEY=`cat API_KEY`

wget "https://na1.api.riotgames.com/lol/static-data/v3/items?locale=en_US&tags=all&api_key=$API_KEY" -O riot/items.json
