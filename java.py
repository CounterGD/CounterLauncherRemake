import os
import json
import urllib.request
import platform
import tarfile


class MinecraftJavaDownloader:

    def __init__(
        self,
        minecraft_dir=".minecraft",
        version="latest",
        install_dir="runtime"
    ):
        self.minecraft_dir = minecraft_dir
        self.version = version
        self.install_dir = install_dir

        self.version_json = self.load_version_json()

    def load_version_json(self):
        path = os.path.join(
            self.minecraft_dir,
            "versions",
            self.version,
            f"{self.version}.json"
        )

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Version JSON not found: {path}"
            )

        print(f"[*] Loading version JSON: {path}")

        with open(path, "r") as f:
            return json.load(f)

    def get_required_java(self):
        java = self.version_json.get("javaVersion")

        if java:
            return java["majorVersion"]

        return 8

    def get_os(self):
        system = platform.system().lower()

        if system == "linux":
            return "linux"
        elif system == "windows":
            return "windows"
        elif system == "darwin":
            return "mac"

        raise RuntimeError(
            f"Unsupported OS: {system}"
        )

    def get_arch(self):
        machine = platform.machine().lower()

        if machine in ("aarch64", "arm64"):
            return "aarch64"

        if machine in ("x86_64", "amd64"):
            return "x64"

        raise RuntimeError(
            f"Unsupported architecture: {machine}"
        )

    def download_runtime(self):

        java_version = self.get_required_java()
        os_name = self.get_os()
        arch = self.get_arch()

        print(f"Required Java: {java_version}")
        print(f"Platform: {os_name}-{arch}")

    def get_microsoft_url(self):
        java_version = self.get_required_java()

        os_name = self.get_os()
        arch = self.get_arch()

        if os_name == "linux" and arch == "aarch64":
            return (
                f"https://aka.ms/download-jdk/"
                f"microsoft-jdk-{java_version}-linux-aarch64.tar.gz"
            )

        if os_name == "linux" and arch == "x64":
            return (
                f"https://aka.ms/download-jdk/"
                f"microsoft-jdk-{java_version}-linux-x64.tar.gz"
            )

        if os_name == "windows" and arch == "x64":
            return (
                f"https://aka.ms/download-jdk/"
                f"microsoft-jdk-{java_version}-windows-x64.zip"
            )

        raise RuntimeError(
            f"Unsupported Microsoft OpenJDK target: {os_name}-{arch}"
        )

    def download_runtime(self):

        java_version = self.get_required_java()

        print(f"Required Java: {java_version}")

        url = self.get_microsoft_url()

        print("[*] Downloading Microsoft OpenJDK:")
        print(url)

        os.makedirs(
            self.install_dir,
            exist_ok=True
        )

        archive = os.path.join(
            self.install_dir,
            f"microsoft-jdk-{java_version}.tar.gz"
        )

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "MinecraftLauncher/1.0"
            }
        )

        with urllib.request.urlopen(request) as response:
            with open(archive, "wb") as f:
                f.write(response.read())

        print("[+] Downloaded:")
        print(archive)

        print("[*] Extracting...")

        with tarfile.open(
            archive,
            "r:gz"
        ) as tar:
            tar.extractall(
                self.install_dir,
                filter="data"
            )

        print("[+] Java installed:")
        print(self.install_dir)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Download the required Java runtime for Minecraft"
    )

    parser.add_argument(
        "version",
        help="Minecraft version (example: 26.2)"
    )

    parser.add_argument(
        "--minecraft-dir",
        default=".minecraft",
        help="Minecraft directory (default: .minecraft)"
    )

    args = parser.parse_args()

    downloader = MinecraftJavaDownloader(
        minecraft_dir=args.minecraft_dir,
        version=args.version
    )

    downloader.download_runtime()
