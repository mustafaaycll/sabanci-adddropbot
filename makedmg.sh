#!/bin/sh
# Create a .spec file containing info about dependencies
pyi-makespec main.py \
  --onefile \
  --noconsole \
  --add-binary "./driver/chromedriver:driver" \
  --add-data "./assets/logo.png:assets" \
  --add-data "./assets/visibility_off.png:assets" \
  --add-data "./assets/visibility_on.png:assets"  \
  --add-data "./ui/main.ui:ui" \
  --add-data "./ui/second.ui:ui" \
  --name "subot" \
  --icon "assets/subot.icns"
# Create executable using the .spec file
pyinstaller subot.spec
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
  --volicon "assets/subot.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "subot.app" 175 120 \
  --hide-extension "subot.app" \
  --app-drop-link 425 120 \
  "dist/subot.dmg" \
  "dist/dmg/"