import json
import os
import urllib.request
from java import MinecraftJavaDownloader
from libs import *

VERSION_MANIFEST = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

user_input = input("Minecraft version or manifest URL: ").strip()

if user_input.startswith("http://") or user_input.startswith("https://"):
    MANIFEST_URL = user_input
else:
    print(f"[*] Looking up Minecraft {user_input}...")

    with urllib.request.urlopen(VERSION_MANIFEST) as r:
        version_manifest = json.load(r)

    version_info = None

    for version in version_manifest["versions"]:
        if version["id"] == user_input:
            version_info = version
            break

    if version_info is None:
        print(f"[!] Version '{user_input}' not found.")
        exit(1)

    with urllib.request.urlopen(version_info["url"]) as r:
        version_json = json.load(r)

    MANIFEST_URL = version_json["assetIndex"]["url"]

print(f"[*] Asset manifest: {MANIFEST_URL}")

ASSETS_DIR = "assets"
INDEX_DIR = os.path.join(ASSETS_DIR, "indexes")
OBJECTS_DIR = os.path.join(ASSETS_DIR, "objects")

os.makedirs(INDEX_DIR, exist_ok=True)
os.makedirs(OBJECTS_DIR, exist_ok=True)

index_name = os.path.basename(MANIFEST_URL)

print("[*] Downloading asset index...")

index_path = os.path.join(INDEX_DIR, index_name)

urllib.request.urlretrieve(MANIFEST_URL, index_path)

with open(index_path, "r", encoding="utf-8") as f:
    index = json.load(f)

objects = index["objects"]

print(f"[*] {len(objects)} assets found.")

downloaded = 0
skipped = 0

for name, asset in objects.items():
    sha1 = asset["hash"]
    prefix = sha1[:2]

    folder = os.path.join(OBJECTS_DIR, prefix)
    os.makedirs(folder, exist_ok=True)

    outfile = os.path.join(folder, sha1)

    if os.path.exists(outfile):
        skipped += 1
        continue

    url = f"https://resources.download.minecraft.net/{prefix}/{sha1}"

    try:
        urllib.request.urlretrieve(url, outfile)
        downloaded += 1
        print(f"[{downloaded}/{len(objects)}] {name}")
    except Exception as e:
        print(f"[!] Failed: {name}")
        print(e)

print("\nDone!")
print(f"Downloaded: {downloaded}")
print(f"Skipped: {skipped}")
