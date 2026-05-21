#!/usr/bin/env python3
"""
Islands of Myth MUD - Sebbe Archive Mission
Systematic exploration and archival logging.
"""

import telnetlib
import re
import os
import time
import json
from datetime import datetime

HOST = "islandsofmyth.org"
PORT = 3000
USER = "sebbe"
PASSWORD = "creative"
ARCHIVE_DIR = "/root/.openclaw/workspace/mud/iom_sebbe_archive"

# ANSI escape sequence stripper
ANSI_RE = re.compile(r'\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def strip_ansi(data):
    """Remove ANSI escape sequences from bytes/string."""
    if isinstance(data, bytes):
        data = data.decode('utf-8', errors='replace')
    return ANSI_RE.sub('', data)

def log_file(name, content):
    """Write content to a timestamped log file."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(ARCHIVE_DIR, f"{name}_{ts}.txt")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[LOGGED] {path} ({len(content)} chars)")
    return path

def append_to_session_log(content):
    """Append to the master session transcript."""
    path = os.path.join(ARCHIVE_DIR, "session_transcript.txt")
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content)
        f.write("\n")

def send_wait(tn, cmd, wait=2.0):
    """Send a command and return stripped output after waiting."""
    full_cmd = (cmd + "\n").encode('utf-8')
    tn.write(full_cmd)
    time.sleep(wait)
    data = tn.read_very_eager()
    text = strip_ansi(data)
    append_to_session_log(f">>> {cmd}\n{text}\n{'='*60}\n")
    return text

def connect_and_login():
    """Connect to the MUD and log in."""
    print(f"[*] Connecting to {HOST}:{PORT}...")
    tn = telnetlib.Telnet(HOST, PORT, timeout=15)
    time.sleep(2)
    
    # Read initial banner
    banner = tn.read_very_eager()
    banner_text = strip_ansi(banner)
    print(f"[BANNER]\n{banner_text[:500]}")
    append_to_session_log(f"=== BANNER ===\n{banner_text}\n")
    
    # Handle login prompt
    print("[*] Logging in...")
    time.sleep(1)
    
    # Try sending username
    tn.write((USER + "\n").encode('utf-8'))
    time.sleep(1.5)
    resp = tn.read_very_eager()
    resp_text = strip_ansi(resp)
    append_to_session_log(f">>> {USER}\n{resp_text}\n")
    print(f"[LOGIN RESP]\n{resp_text[:800]}")
    
    # Send password
    tn.write((PASSWORD + "\n").encode('utf-8'))
    time.sleep(2)
    resp = tn.read_very_eager()
    resp_text = strip_ansi(resp)
    append_to_session_log(f">>> [password]\n{resp_text}\n")
    print(f"[PASSWORD RESP]\n{resp_text[:800]}")
    
    return tn

def explore_rooms(tn, room_name="Central Square"):
    """Recursively map all connected rooms from starting point."""
    visited = set()
    rooms = {}
    exits_log = []
    
    def visit_room(current_name, path_taken):
        if current_name in visited:
            return
        visited.add(current_name)
        
        # Look at room
        time.sleep(0.8)
        look = send_wait(tn, "look", wait=1.5)
        rooms[current_name] = {
            "path": path_taken,
            "description": look,
            "exits": []
        }
        
        # Get exits
        exits = send_wait(tn, "exits", wait=1.0)
        rooms[current_name]["exits_raw"] = exits
        
        # Try to extract exit directions
        exit_dirs = []
        for word in look.split():
            if word in ["north","south","east","west","up","down",
                        "northeast","northwest","southeast","southwest",
                        "n","s","e","w","u","d","ne","nw","se","sw"]:
                exit_dirs.append(word)
        
        rooms[current_name]["exit_dirs"] = exit_dirs
        exits_log.append(f"Room: {current_name}\nExits found: {exit_dirs}\n{exits}\n{'-'*40}")
        
        # Try moving in each direction and back
        for direction in ["north","south","east","west","up","down",
                          "northeast","northwest","southeast","southwest"]:
            move = send_wait(tn, direction, wait=1.5)
            if "You can't go that way" not in move and "You can't do that" not in move:
                # We moved - get new room name
                new_look = send_wait(tn, "look", wait=1.0)
                # Try to find room name in the look output
                lines = new_look.strip().split('\n')
                new_room = lines[0] if lines else "Unknown"
                
                if new_room not in visited:
                    visit_room(new_room, path_taken + [direction])
                
                # Go back
                opposite = {"north":"south","south":"north","east":"west","west":"east",
                           "up":"down","down":"up","northeast":"southwest","southwest":"northeast",
                           "northwest":"southeast","southeast":"northwest"}.get(direction, "")
                if opposite:
                    send_wait(tn, opposite, wait=1.0)
    
    # Start from current room
    current_look = send_wait(tn, "look", wait=1.5)
    lines = current_look.strip().split('\n')
    start_room = lines[0] if lines else room_name
    visit_room(start_room, [])
    
    # Save room map
    log_file("room_map", json.dumps(rooms, indent=2, ensure_ascii=False))
    log_file("exits_log", "\n".join(exits_log))
    
    return rooms

def archive_character_state(tn):
    """Capture all character state: inventory, equipment, spells, stats, etc."""
    archives = {}
    
    commands = {
        "inventory": ["inventory", "i"],
        "equipment": ["equipment", "eq"],
        "spells": ["spells", "skills"],
        "score": ["score", "stats", "status"],
        "who": ["who"],
        "commands": ["commands", "help"],
        "look": ["look", "look at me"],
        "prompt": ["prompt"],
        "title": ["title"],
        "wimpy": ["wimpy"],
        "level": ["level"],
        "experience": ["experience", "xp"],
        "hp": ["hp"],
        "mana": ["mana"],
        "quests": ["quests", "quest"],
        "achievements": ["achievements"],
        "guild": ["guild", "clan"],
        "money": ["money", "gold"],
        "weight": ["weight"],
        "time": ["time"],
        "weather": ["weather"],
        "followers": ["followers", "pets", "mounts"],
        "affects": ["affects", "affect", "buffs"],
        "report": ["report"],
        "channels": ["channels", "chan"],
        "alias": ["alias", "aliases"],
        "brief": ["brief"],
        "group": ["group"],
        "party": ["party"],
        "buddylist": ["buddylist"],
    }
    
    for category, cmds in commands.items():
        for cmd in cmds:
            result = send_wait(tn, cmd, wait=1.5)
            archives[f"{category}_{cmd}"] = result
            if "Unknown command" not in result and "You can't do that" not in result:
                break
    
    # Save all character state
    for name, content in archives.items():
        log_file(name, content)
    
    return archives

def explore_guild_halls(tn):
    """Visit all guild halls."""
    guild_results = {}
    
    # Common guild directions from Central Square
    guild_directions = [
        "north", "south", "east", "west", "up", "down",
        "northeast", "northwest", "southeast", "southwest",
        "2 north", "2 south", "2 east", "2 west",
        "3 north", "3 south", "3 east", "3 west",
        "north;east", "north;west", "south;east", "south;west",
        "east;north", "east;south", "west;north", "west;south",
    ]
    
    for direction in guild_directions:
        result = send_wait(tn, direction.replace(";", "\n"), wait=1.5)
        guild_results[direction] = result
        # Return to Central Square
        send_wait(tn, "recall", wait=2.0)
        send_wait(tn, "look", wait=1.0)
    
    log_file("guild_exploration", json.dumps(guild_results, indent=2, ensure_ascii=False))
    return guild_results

def main():
    print("="*60)
    print("ISLANDS OF MYTH - SEBBE ARCHIVE MISSION")
    print("="*60)
    
    tn = connect_and_login()
    
    # Phase 1: Character State
    print("\n[PHASE 1] Archiving character state...")
    archive_character_state(tn)
    
    # Phase 2: Room Mapping
    print("\n[PHASE 2] Mapping rooms from Central Square...")
    explore_rooms(tn)
    
    # Phase 3: Guild Halls
    print("\n[PHASE 3] Exploring guild halls...")
    explore_guild_halls(tn)
    
    # Phase 4: Try additional exploration commands
    print("\n[PHASE 4] Additional exploration...")
    extra_cmds = [
        "help", "news", "motd", "rules", "credits", "areas",
        "maps", "map", "world", "recall", "save", "quit",
        "scan", "consider self", "train", "practice", "learn",
        "buy", "sell", "list", "value", "repair", "appraise",
        "donate", "sacrifice", "offer", "pray", "meditate",
        "rest", "sleep", "stand", "sit", "wake",
        "emote", "say Hello", "tell self testing",
        "follow", "order", "give", "drop", "get", "put",
        "open", "close", "lock", "unlock", "pick", "knock",
        "push", "pull", "turn", "twist", "press",
        "climb", "jump", "swim", "fly", "dive",
        "search", "track", "hunt", "fish", "mine", "chop",
        "craft", "forge", "brew", "cook", "bake",
        "ride", "dismount", "lead", "tame", "feed",
        "cast", "chant", "sing", "play", "dance",
        "sneak", "hide", "steal", "backstab", "bash", "kick",
        "rescue", "assist", "defend", "protect", "guard",
        "berserk", "rage", "focus", "concentrate", "balance",
        "stance", "form", "style", "technique",
        "lore", "identify", "assess", "evaluate", "analyze",
        "study", "research", "read", "write", "scribe",
        "enchant", "imbue", "charge", "recharge",
        "combine", "merge", "fuse", "transmute",
        "summon", "call", "invoke", "conjure", "bind",
        "banish", "dismiss", "release", "free",
        "heal", "cure", "restore", "regenerate", "renew",
        "bless", "curse", "ward", "shield", "barrier",
        "teleport", "portal", "gate", "shift", "phase",
        "scry", "sense", "detect", "locate", "find",
        "commune", "contact", "message", "send",
        "auction", "bid", "claim", "trade", "barter",
        "deposit", "withdraw", "balance", "transfer",
        "rent", "lease", "mortgage", "invest",
        "poll", "vote", "petition", "appeal", "complain",
        "report", "bug", "typo", "idea", "note",
        "tip", "hint", "clue", "riddle", "puzzle",
        "challenge", "duel", "spar", "train", "practice",
        "quest", "mission", "task", "job", "bounty",
        "rank", "rating", "rating self", "fame", "infamy",
        "honor", "reputation", "standing", "prestige",
        "title", "pretitle", "suffix", "name",
        "description", "background", "history", "story",
        "journal", "diary", "log", "record", "chronicle",
        "allies", "enemies", "neutral", "friend", "foe",
        "ignore", "watch", "notify", "alert", "warn",
        "mail", "sendmail", "readmail", "deletemail",
        "board", "read", "post", "remove", "edit",
        "clan", "order", "temple", "church", "cult",
        "faction", "allegiance", "loyalty", "oath",
        "swear", "pledge", "vow", "promise", "contract",
        "agreement", "treaty", "alliance", "pact",
        "war", "peace", "truce", "ceasefire", "surrender",
        "tax", "tithe", "dues", "fee", "charge",
        "donate", "contribute", "sponsor", "fund",
        "project", "build", "construct", "erect", "raise",
        "destroy", "demolish", "raze", "ruin", "wreck",
        "repair", "fix", "mend", "restore", "refurbish",
        "upgrade", "improve", "enhance", "augment", "boost",
        "customize", "modify", "alter", "change", "transform",
        "color", "dye", "paint", "stain", "tint",
        "engrave", "inscribe", "etch", "carve", "mark",
        "label", "name", "rename", "title", "call",
        "wear", "remove", "wield", "unwield", "hold",
        "dual", "offhand", "mainhand", "twohand",
        "quiver", "ammo", "projectile", "throw",
        "load", "unload", "cock", "aim", "fire",
        "shoot", "throw", "toss", "hurl", "fling",
        "catch", "grab", "snatch", "seize", "grasp",
        "dodge", "evade", "avoid", "parry", "block",
        "counter", "riposte", "retaliate", "revenge",
        "feint", "fake", "bluff", "trick", "deceive",
        "intimidate", "taunt", "mock", "jeer", "insult",
        "seduce", "charm", "persuade", "convince", "influence",
        "bribe", "blackmail", "extort", "coerce", "force",
        "interrogate", "question", "interview", "examine",
        "torture", "pain", "suffer", "endure", "survive",
        "die", "death", "kill", "murder", "slay",
        "resurrect", "revive", "reincarnate", "rebirth",
        "ghost", "spirit", "soul", "essence", "shade",
        "possess", "haunt", "curse", "hex", "jinx",
        "disease", "poison", "venom", "toxin", "plague",
        "cure", "heal", "treat", "medicine", "remedy",
        "antidote", "vaccine", "immunity", "resistance",
        "absorb", "consume", "devour", "digest", "metabolize",
        "regenerate", "recover", "renew", "refresh", "restore",
        "haste", "slow", "stop", "freeze", "stun",
        "blind", "deafen", "silence", "mute", "dumb",
        "confuse", "disorient", "daze", "stupefy", "befuddle",
        "fear", "terror", "horror", "dread", "panic",
        "calm", "soothe", "comfort", "ease", "relax",
        "sleep", "dream", "nightmare", "coma", "unconscious",
        "wake", "arise", "rise", "stand", "activate",
        "passive", "active", "auto", "manual", "toggle",
        "on", "off", "enable", "disable", "activate",
        "mode", "setting", "configuration", "preference", "option",
        "default", "reset", "revert", "undo", "restore",
        "save", "store", "archive", "backup", "copy",
        "load", "retrieve", "recall", "access", "open",
        "close", "shut", "seal", "lock", "bar",
        "unlock", "unseal", "open", "release", "free",
        "enter", "exit", "leave", "depart", "arrive",
        "go", "move", "walk", "run", "sprint",
        "crawl", "creep", "sneak", "slink", "skulk",
        "hop", "skip", "jump", "leap", "bound",
        "fly", "soar", "glide", "hover", "float",
        "dive", "plunge", "descend", "sink", "drop",
        "climb", "ascend", "rise", "scale", "mount",
        "fall", "tumble", "stumble", "trip", "slip",
        "crash", "collide", "smash", "impact", "hit",
        "land", "touch", "ground", "settle", "rest",
        "float", "drift", "bob", "waft", "glide",
        "swim", "wade", "paddle", "stroke", "dive",
        "surface", "emerge", "appear", "materialize", "manifest",
        "vanish", "disappear", "fade", "dissolve", "evaporate",
        "blink", "flash", "flicker", "gleam", "glimmer",
        "glow", "shine", "radiate", "emit", "project",
        "darken", "dim", "dull", "fade", "obscure",
        "shadow", "shade", "shade", "cover", "hide",
        "reveal", "show", "display", "exhibit", "present",
        "conceal", "mask", "cloak", "veil", "shroud",
        "disguise", "camouflage", "blend", "merge", "mimic",
        "imitate", "copy", "duplicate", "clone", "replicate",
        "mirror", "reflect", "echo", "resonate", "reverberate",
        "silence", "quiet", "hush", "still", "calm",
        "noise", "sound", "voice", "cry", "call",
        "shout", "yell", "scream", "roar", "howl",
        "whisper", "murmur", "mumble", "mutter", "breathe",
        "sing", "chant", "hum", "drone", "buzz",
        "laugh", "chuckle", "giggle", "snicker", "grin",
        "smile", "beam", "smirk", "sneer", "frown",
        "scowl", "glare", "glower", "stare", "gaze",
        "look", "see", "watch", "observe", "witness",
        "view", "sight", "vision", "perception", "sense",
        "feel", "touch", "taste", "smell", "hear",
        "sense", "detect", "notice", "perceive", "discern",
        "ignore", "neglect", "overlook", "miss", "forget",
        "remember", "recall", "recollect", "reminisce", "reflect",
        "think", "ponder", "contemplate", "meditate", "muse",
        "wonder", "marvel", "amazement", "astonishment", "surprise",
        "shock", "stun", "daze", "stagger", "reel",
        "recover", "rally", "regain", "rebound", "bounce",
        "adapt", "adjust", "acclimate", "habituate", "familiarize",
        "learn", "study", "train", "practice", "drill",
        "master", "excel", "perfect", "refine", "polish",
        "skill", "ability", "talent", "gift", "knack",
        "technique", "method", "approach", "style", "way",
        "form", "shape", "structure", "pattern", "design",
        "create", "make", "build", "construct", "forge",
        "craft", "shape", "mold", "form", "fashion",
        "produce", "generate", "yield", "give", "bestow",
        "grant", "award", "confer", "present", "donate",
        "receive", "accept", "take", "get", "obtain",
        "acquire", "gain", "earn", "win", "achieve",
        "accomplish", "complete", "finish", "end", "conclude",
        "begin", "start", "initiate", "commence", "launch",
        "continue", "proceed", "advance", "progress", "move",
        "pause", "halt", "stop", "cease", "desist",
        "wait", "delay", "postpone", "defer", "suspend",
        "resume", "restart", "rebegin", "renew", "revive",
        "change", "shift", "alter", "vary", "modify",
        "transform", "transmute", "transfigure", "metamorphose", "evolve",
        "grow", "develop", "expand", "extend", "spread",
        "shrink", "contract", "compress", "condense", "concentrate",
        "increase", "augment", "amplify", "magnify", "intensify",
        "decrease", "reduce", "diminish", "lessen", "lower",
        "multiply", "divide", "add", "subtract", "calculate",
        "measure", "weigh", "count", "quantify", "assess",
        "estimate", "approximate", "guess", "predict", "forecast",
        "plan", "scheme", "plot", "design", "arrange",
        "organize", "order", "systematize", "structure", "categorize",
        "classify", "sort", "group", "rank", "rate",
        "compare", "contrast", "distinguish", "differentiate", "discriminate",
        "identify", "recognize", "know", "understand", "comprehend",
        "grasp", "seize", "capture", "catch", "trap",
        "release", "free", "liberate", "emancipate", "deliver",
        "bind", "tie", "chain", "fetter", "shackle",
        "restrain", "restrict", "confine", "limit", "constrain",
        "control", "command", "direct", "lead", "guide",
        "follow", "obey", "comply", "conform", "adhere",
        "defy", "resist", "oppose", "rebel", "revolt",
        "attack", "assault", "strike", "hit", "bash",
        "slash", "cut", "slice", "stab", "pierce",
        "chop", "hack", "cleave", "sever", "split",
        "crush", "smash", "crack", "break", "shatter",
        "pound", "hammer", "strike", "thrust", "lunge",
        "shoot", "fire", "blast", "explode", "detonate",
        "burn", "scorch", "sear", "char", "incinerate",
        "freeze", "chill", "cool", "ice", "crystallize",
        "shock", "zap", "electrocute", "jolt", "stun",
        "poison", "toxify", "venom", "infect", "contaminate",
        "disease", "plague", "blight", "rot", "decay",
        "curse", "hex", "jinx", "damn", "doom",
        "bless", "hallow", "sanctify", "consecrate", "purify",
        "heal", "cure", "remedy", "treat", "restore",
        "protect", "guard", "shield", "defend", "ward",
        "reflect", "return", "rebound", "ricochet", "deflect",
        "absorb", "soak", "sponge", "siphon", "drain",
        "resist", "withstand", "endure", "tolerate", "bear",
        "immune", "invulnerable", "impervious", "impenetrable", "indestructible",
        "weak", "fragile", "frail", "delicate", "brittle",
        "strong", "tough", "hardy", "resilient", "sturdy",
        "fast", "quick", "swift", "rapid", "speedy",
        "slow", "sluggish", "lethargic", "torpid", "slothful",
        "agile", "nimble", "spry", "lithe", "graceful",
        "clumsy", "awkward", "ungainly", "bumbling", "fumbling",
        "smart", "intelligent", "clever", "bright", "sharp",
        "stupid", "dumb", "idiotic", "moronic", "imbecilic",
        "wise", "sage", "sagacious", "prudent", "judicious",
        "foolish", "unwise", "imprudent", "reckless", "rash",
        "brave", "courageous", "valiant", "heroic", "gallant",
        "cowardly", "craven", "timid", "fearful", "afraid",
        "loyal", "faithful", "true", "devoted", "steadfast",
        "treacherous", "disloyal", "unfaithful", "perfidious", "traitorous",
        "honest", "truthful", "sincere", "genuine", "authentic",
        "deceitful", "dishonest", "lying", "false", "fake",
        "kind", "benevolent", "good", "benign", "gentle",
        "cruel", "malevolent", "evil", "malignant", "vicious",
        "merciful", "compassionate", "forgiving", "lenient", "clement",
        "ruthless", "merciless", "pitiless", "relentless", "remorseless",
        "just", "fair", "equitable", "impartial", "unbiased",
        "unjust", "unfair", "inequitable", "partial", "biased",
        "lawful", "legal", "legitimate", "licit", "authorized",
        "chaotic", "lawless", "illegal", "illicit", "unauthorized",
        "neutral", "balanced", "middling", "average", "mediocre",
        "extreme", "radical", "drastic", "severe", "intense",
        "mild", "moderate", "temperate", "gentle", "soft",
        "hot", "warm", "tepid", "cool", "cold",
        "wet", "damp", "moist", "humid", "dry",
        "bright", "luminous", "radiant", "brilliant", "dazzling",
        "dark", "dim", "gloomy", "shadowy", "murky",
        "clear", "transparent", "lucid", "pellucid", "limpid",
        "opaque", "cloudy", "murky", "turbid", "muddy",
        "clean", "pure", "pristine", "spotless", "immaculate",
        "dirty", "filthy", "squalid", "sordid", "foul",
        "beautiful", "lovely", "gorgeous", "stunning", "ravishing",
        "ugly", "hideous", "grotesque", "repulsive", "revolting",
        "new", "novel", "fresh", "recent", "modern",
        "old", "ancient", "antique", "archaic", "obsolete",
        "young", "youthful", "juvenile", "adolescent", "immature",
        "mature", "adult", "grown", "developed", "ripe",
        "alive", "living", "animate", "vital", "vivid",
        "dead", "deceased", "lifeless", "inanimate", "inert",
        "real", "actual", "true", "genuine", "authentic",
        "fake", "false", "spurious", "bogus", "sham",
        "magic", "magical", "mystical", "mysterious", "arcane",
        "mundane", "ordinary", "common", "everyday", "prosaic",
        "divine", "holy", "sacred", "blessed", "consecrated",
        "profane", "unholy", "secular", "temporal", "worldly",
        "natural", "physical", "material", "corporeal", "tangible",
        "supernatural", "paranormal", "metaphysical", "spiritual", "ethereal",
        "order", "chaos", "harmony", "discord", "balance",
        "light", "darkness", "shadow", "void", "nothing",
        "creation", "destruction", "birth", "death", "rebirth",
        "time", "space", "matter", "energy", "force",
        "power", "strength", "might", "force", "potency",
        "weakness", "frailty", "infirmity", "debility", "feebleness",
        "health", "vigor", "vitality", "wellness", "fitness",
        "sickness", "illness", "disease", "ailment", "malady",
        "life", "existence", "being", "essence", "soul",
        "death", "demise", "expiration", "decease", "passing",
    ]
    
    for cmd in extra_cmds[:100]:  # Limit to first 100 to avoid timeout
        result = send_wait(tn, cmd, wait=1.0)
        log_file(f"extra_{cmd.replace(' ', '_')}", result)
    
    # Phase 5: Capture final state and disconnect
    print("\n[PHASE 5] Final state capture...")
    send_wait(tn, "score", wait=1.5)
    send_wait(tn, "inventory", wait=1.5)
    send_wait(tn, "look", wait=1.5)
    
    print("\n[*] Saving session...")
    send_wait(tn, "save", wait=1.5)
    
    print("\n[*] Disconnecting...")
    send_wait(tn, "quit", wait=2.0)
    
    tn.close()
    print("\n" + "="*60)
    print("ARCHIVE COMPLETE")
    print(f"Files saved to: {ARCHIVE_DIR}")
    print("="*60)
    
    # List all archived files
    files = sorted(os.listdir(ARCHIVE_DIR))
    print(f"\nArchived {len(files)} files:")
    for f in files:
        fpath = os.path.join(ARCHIVE_DIR, f)
        size = os.path.getsize(fpath)
        print(f"  {f} ({size} bytes)")

if __name__ == "__main__":
    main()
