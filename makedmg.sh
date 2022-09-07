#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/subot.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/subot.dmg" && rm "dist/subot.dmg"
create-dmg \
  --volname "subot" \
  --volicon "subot.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "subot.app" 175 120 \
  --hide-extension "subot.app" \
  --app-drop-link 425 120 \
  "dist/subot.dmg" \
  "dist/dmg/"