#!/bin/bash
# Fetch all IOM guild pages

BASE="http://www.islandsofmyth.org/3k/cgi/guildtree.c?name="
OUTDIR="/root/.openclaw/workspace/reddragon/docs/guilds"

# All guild names (spaces become +)
guilds=(
  # Warrior Tree
  warrior knight defender_of_the_crown berserker traveler
  blade_dancer barbarian shield_master flogger thruster champion_of_the_crown
  # Martial Artist Tree
  "martial artist" dragonfist mystic fighter warriors
  "toad master" "tiger master" "crane master" "snake master" "order of the crescent moon" "dragon master"
  # Acrobat Tree
  acrobat "street brawler" juggler bard
  minstrel bartender bannerman gleeman troubadour
  # Abjurer Tree
  abjurer "protector of the earth" "masters of energy" irrifletta navigator
  "master abjurer" "harbinger of anguish" enchanter "master navigators"
  "master of disruption" guardians
  # Psychics Tree
  psychics mystics witch telekinetics
  "cauldron magic" oneiromancers "watchers of the night" psionists
  "talisman magic"
  # Elemental Tree
  elemental "fire mage" "earth mage" "air mage" "water mage"
  "lava mage" "mist mage" "nether mage"
  # Necromancer Tree
  necromancer necroscope voodooist "bone mage"
  "stygian sorcerer" embalmer dreadlord scourge
  "lords of undeath" "blood brother"
  # Evoker Tree
  evoker "evoker of elements" "evoker of ether"
  "evoker of magic" "evoker of vacuum" "evoker of flames" "evoker of force"
  "evoker of poison" "evoker of acid" "evoker of lightning" "evoker of ice"
  sorcerer
  # Weaver Tree
  weaver healer martyr confessor
  avatar exorcist templar "shields of faith"
  "high priest"
  # Unraveller Tree
  unraveller harmer sacrificer "magical torturer"
  "servant of mordulak" "servant of shirija" "servant of talakh" "servant of lloth"
  "elder of mordulak" "patriarch of shirija" "sword of talakh" "primate of lloth" "master enchanter"
  # Druid Tree
  druid "weather watcher" "animal tamer" herbalist
  "adept of the stones" "shaman of soil"
  "chanter of deep earth"
  # Shapeshifter Tree
  shapeshifter "bestial seccedaneum" savager
  "animal healer" "animal trainer" "beast lord" "dragon lord"
  # Woodsman Tree
  woodsman "sylvan guard" "sylvan ward"
  "sylvan scout" "sylvan protector" "sylvan woodlord"
  # Lurker Tree
  lurker "poison brewer" trickster
  assassin "master assassin" "disciple of shadow"
  "silent hand"
)

for guild in "${guilds[@]}"; do
  # Create URL-safe and filename-safe versions
  url_name=$(echo "$guild" | sed 's/ /+/g')
  file_id=$(echo "$guild" | tr ' ' '_' | tr -cd 'a-zA-Z0-9_')
  
  echo "Fetching: $guild -> $file_id.md"
  
  # Try multiple times
  for i in 1 2 3; do
    if curl -sS --max-time 30 "${BASE}${url_name}" > "$OUTDIR/${file_id}.tmp" 2>/dev/null; then
      # Check if we got actual content (not empty or error)
      if [ -s "$OUTDIR/${file_id}.tmp" ] && ! grep -q "Not Found\|Error\|404" "$OUTDIR/${file_id}.tmp"; then
        mv "$OUTDIR/${file_id}.tmp" "$OUTDIR/${file_id}.md"
        echo "  OK ($(wc -c < "$OUTDIR/${file_id}.md") bytes)"
        break
      fi
    fi
    sleep 2
  done
  
  if [ -f "$OUTDIR/${file_id}.tmp" ]; then
    rm "$OUTDIR/${file_id}.tmp"
    echo "  FAILED"
  fi
  
  # Small delay to be polite
  sleep 0.5
done

echo "Done. Files fetched:"
ls -la "$OUTDIR"/*.md 2>/dev/null | wc -l
echo "Files missing:"
ls -la "$OUTDIR"/*.tmp 2>/dev/null | wc -l
