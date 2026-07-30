	#!/usr/bin/env python3

import shutil
import json
import os
import urllib.request
import platform
import zipfile

VERSION_MANIFEST_URL = (
    "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
)

class LaunchScriptGenerator:

    def __init__(self, version_json):
        self.version_json = version_json

    def generate(self):
        self.generate_linux()
        self.generate_windows()

    def generate_windows(self):

        main = self.version_json["mainClass"]

        script = f"""@echo off

set /p CP=<classpath.txt

java ^
    -cp "%CP%" ^
    -Djava.library.path=natives ^
    {main} %*
    """

        with open("launch.bat", "w", newline="\r\n") as f:
            f.write(script)

    def generate_linux(self):

        main = self.version_json["mainClass"]

        script = f"""#!/bin/sh

CP="$(cat classpath.txt)"

java \\
    -cp "$CP" \\
    -Djava.library.path=natives \\
    {main} "$@"
"""

        with open("launch.sh", "w", newline="\n") as f:
            f.write(script)

        os.chmod("launch.sh", 0o755)

class ClasspathBuilder:

    def __init__(self, classpath, version_json):
        self.classpath = list(classpath)
        self.version_json = version_json

    def build(self):

        version = self.version_json["id"]

        client = os.path.join(
            "versions",
            version,
            f"{version}.jar"
        )

        if os.path.exists(client):
            self.classpath.append(client)

        separator = ";" if os.name == "nt" else ":"

        with open("classpath.txt", "w", encoding="utf-8") as f:
            f.write(separator.join(self.classpath))

        print("[+] Generated classpath.txt")

        return self.classpath

class NativeDownloader:

    def __init__(self, version_json):
        self.version_json = version_json

    def get_classifier(self):

        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == "windows":
            return "natives-windows"

        if system == "darwin":
            return "natives-macos"

        if system == "linux":

            if machine in (
                "aarch64",
                "arm64",
            ):
                return "natives-linux-arm64"

            return "natives-linux"

        raise RuntimeError(f"Unsupported platform: {system}")

    def download_all(self):

        classifier = self.get_classifier()

        print(f"[*] Native classifier: {classifier}")

        for library in self.version_json.get("libraries", []):

            downloads = library.get("downloads", {})
            classifiers = downloads.get("classifiers")

            if classifiers is None:
                continue

            native = classifiers.get(classifier)

            if native is None:
                continue

            self.download_native(native, library)

    def download_native(self, native, library):

        outfile = os.path.join(
            "libraries",
            native["path"]
        )

        os.makedirs(
            os.path.dirname(outfile),
            exist_ok=True
        )

        if not os.path.exists(outfile):

            print(f"[↓] {native['path']}")

            urllib.request.urlretrieve(
                native["url"],
                outfile
            )

        self.extract(outfile, library)

    def extract(self, jar, library):

        os.makedirs("natives", exist_ok=True)

        excludes = (
            library
            .get("extract", {})
            .get("exclude", [])
        )

        with zipfile.ZipFile(jar) as archive:

            for member in archive.namelist():

                skip = False

                for exclude in excludes:
                    if member.startswith(exclude):
                        skip = True
                        break

                if skip:
                    continue

                if member.endswith("/"):
                    continue

                archive.extract(member, "natives")

class LibraryDownloader:

    def __init__(self, version_json):
        self.version_json = version_json
        self.classpath = []

    def download_all(self):

        libraries = self.version_json.get("libraries", [])

        print(f"[*] Downloading {len(libraries)} libraries...")

        for library in libraries:

            downloads = library.get("downloads", {})

            artifact = downloads.get("artifact")

            if artifact is None:
                continue

            self.download_artifact(artifact)

        print()
        print(f"[+] Downloaded {len(self.classpath)} libraries.")

        return self.classpath

    def download_artifact(self, artifact):

        path = artifact["path"]
        url = artifact["url"]

        outfile = os.path.join("libraries", path)

        os.makedirs(os.path.dirname(outfile), exist_ok=True)

        if os.path.exists(outfile):
            print(f"[=] {path}")
            self.classpath.append(outfile)
            return

        print(f"[↓] {path}")

        urllib.request.urlretrieve(url, outfile)

        self.classpath.append(outfile)

class VersionResolver:
    def __init__(self):
        self.manifest = None

    def load_manifest(self):
        print("[*] Downloading Mojang version manifest...")

        with urllib.request.urlopen(VERSION_MANIFEST_URL) as response:
            self.manifest = json.load(response)

    def resolve(self, version):
        if self.manifest is None:
            self.load_manifest()

        version = version.lower()

        if version == "latest":
            version = self.manifest["latest"]["release"]

        elif version == "snapshot":
            version = self.manifest["latest"]["snapshot"]

        for entry in self.manifest["versions"]:
            if entry["id"] == version:
                return entry

        return None


class VersionDownloader:
    def __init__(self, version_info):
        self.version_info = version_info

    def download(self):
        version = self.version_info["id"]
        url = self.version_info["url"]

        directory = os.path.join("versions", version)
        os.makedirs(directory, exist_ok=True)

        outfile = os.path.join(directory, f"{version}.json")

        print(f"[*] Downloading {version}.json")

        urllib.request.urlretrieve(url, outfile)

        print(f"[+] Saved -> {outfile}")

        with open(outfile, "r", encoding="utf-8") as f:
            return json.load(f)


def download_from_url(url):
    print("[*] Downloading version JSON...")

    with urllib.request.urlopen(url) as response:
        version_json = json.load(response)

    version = version_json["id"]

    directory = os.path.join("versions", version)
    os.makedirs(directory, exist_ok=True)

    outfile = os.path.join(directory, f"{version}.json")

    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(version_json, f, indent=4)

    print(f"[+] Saved -> {outfile}")

    return version_json


def resolve_version(target):
    if target.startswith(("http://", "https://")):
        return download_from_url(target)

    resolver = VersionResolver()

    version_info = resolver.resolve(target)

    if version_info is None:
        raise ValueError(f"Version '{target}' not found.")

    downloader = VersionDownloader(version_info)

    return downloader.download()


def print_info(version_json):
    print()
    print("========== Minecraft Version ==========")
    print(f"ID         : {version_json['id']}")
    print(f"Type       : {version_json.get('type', 'unknown')}")
    print(f"Assets     : {version_json.get('assets', 'unknown')}")
    print(f"Main Class : {version_json.get('mainClass', 'unknown')}")

    if "javaVersion" in version_json:
        print(f"Java       : {version_json['javaVersion']['majorVersion']}")

    if "inheritsFrom" in version_json:
        print(f"Inherits   : {version_json['inheritsFrom']}")

    print(f"Libraries  : {len(version_json.get('libraries', []))}")
    print("=======================================")

def run(target):
    version_json = resolve_version(target)

    library_downloader = LibraryDownloader(version_json)
    classpath = library_downloader.download_all()

    native_downloader = NativeDownloader(version_json)
    native_downloader.download_all()

    classpath_builder = ClasspathBuilder(classpath, version_json)
    classpath = classpath_builder.build()

    launch_generator = LaunchScriptGenerator(version_json)
    launch_generator.generate()

    print_info(version_json)

    return {
        "version": version_json,
        "classpath": classpath
    }

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Minecraft Library Downloader")
        print()
        print("Usage:")
        print("    python mclibs.py <version>")
        print("    python mclibs.py <version JSON URL>")
        print()
        print("Examples:")
        print("    python mclibs.py 1.12.2")
        print("    python mclibs.py latest")
        print("    python mclibs.py snapshot")
        sys.exit(1)

    run(sys.argv[1])
