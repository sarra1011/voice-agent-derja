from voiceagent.dataset import build_manifest

if __name__ == "__main__":
    n = build_manifest()
    print(f"data/manifest.csv written with {n} recordings")
