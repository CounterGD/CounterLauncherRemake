import os
import subprocess


class MinecraftLauncher:
    def __init__(self, minecraft_dir, version):
        self.minecraft_dir = minecraft_dir
        self.version = version

        version_path = os.path.join(
            minecraft_dir,
            "versions",
            version,
            f"{version}.json"
        )

        with open(version_path, "r", encoding="utf-8") as f:
            import json
            self.version_json = json.load(f)

    def get_java(self):
        java_major = self.version_json.get(
            "javaVersion",
            {}
        ).get(
            "majorVersion",
            8
        )

        java_name = "java.exe" if os.name == "nt" else "java"

        return os.path.join(
            self.minecraft_dir,
            "runtimes",
            f"java{java_major}",
            "bin",
            java_name
        )

    def get_natives(self):
        return os.path.join(
            self.minecraft_dir,
            "versions",
            self.version,
            "natives"
        )

    def build_classpath(self):
        sep = ";" if os.name == "nt" else ":"
        cp = []

        for library in self.version_json.get("libraries", []):
            artifact = (
                library.get("downloads", {})
                       .get("artifact")
            )

            if artifact:
                cp.append(
                    os.path.join(
                        self.minecraft_dir,
                        "libraries",
                        artifact["path"]
                    )
                )

        cp.append(
            os.path.join(
                self.minecraft_dir,
                "versions",
                self.version,
                f"{self.version}.jar"
            )
        )

        return sep.join(cp)

    def launch(self,
               username="Player",
               uuid="",
               access_token="0",
               xms="512M",
               xmx="2G"):

        java = self.get_java()

        natives = self.get_natives()

        classpath = self.build_classpath()

        assets_index = self.version_json["assetIndex"]["id"]

        cmd = [
            java,

            f"-Xms{xms}",
            f"-Xmx{xmx}",

            f"-Djava.library.path={natives}",

            "-cp",
            classpath,

            self.version_json["mainClass"],

            "--username", username,
            "--version", self.version,
            "--gameDir", self.minecraft_dir,
            "--assetsDir", os.path.join(
                self.minecraft_dir,
                "assets"
            ),
            "--assetIndex", assets_index,
            "--uuid", uuid,
            "--accessToken", access_token,
            "--userType", "legacy"
        ]

        print("Launching Minecraft...")
        print(" ".join(cmd))

        subprocess.run(cmd)


if __name__ == "__main__":
    launcher = MinecraftLauncher(
        minecraft_dir=".minecraft",
        version="26.2"
    )

    launcher.launch()
