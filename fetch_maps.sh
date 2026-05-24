#!/bin/bash
# Fetch all IOM maps

mkdir -p /root/.openclaw/workspace/iom_maps

cd /root/.openclaw/workspace/iom_maps

for map in gossamer sombre darkcaverns hyboria southcape emerald mists twin_islands everrest oddworld; do
    echo "Fetching $map..."
    curl -s "http://iommud.silvanthalas.com/maps/${map}.html" > "${map}.html"
done

echo "Done fetching maps"
ls -la
