"""SUPERSEDED 31 Oct 2026 by motion/ (kinetic-type engine: motion/reel.html + motion/render.js + motion/reels.json).
Kept for reference only.

Turn rendered reel scenes (1080x1920 PNG) into silent MP4 reels with a slow zoom and crossfades.

python3 reels.py <scenes-root> <out-dir>
Scenes come from creatives.py (<out>/_reel-scenes/<slug>/scene-01.png ... scene-end.png).
Audio: none. Add a track from Instagram's library in the app if wanted (licensing stays with Meta).
"""
import glob
import os
import subprocess
import sys

SCENE, FADE, FPS = 3.6, 0.5, 30


def build(scene_dir, out):
    imgs = sorted(glob.glob(os.path.join(scene_dir, "scene-[0-9]*.png"))) + [os.path.join(scene_dir, "scene-end.png")]
    args, filters = [], []
    for i, im in enumerate(imgs):
        dur = SCENE + (1.0 if im.endswith("end.png") else 0)
        args += ["-i", im]
        frames = int(dur * FPS)
        filters.append(f"[{i}:v]scale=1188:2112,zoompan=z='min(1+0.0009*on,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={FPS},format=yuv420p,setsar=1[v{i}]")
    prev, offset = "v0", SCENE - FADE
    for i in range(1, len(imgs)):
        filters.append(f"[{prev}][v{i}]xfade=transition=fade:duration={FADE}:offset={offset:.2f}[x{i}]")
        prev = f"x{i}"
        offset += SCENE - FADE
    cmd = ["ffmpeg", "-loglevel", "error", "-y", *args, "-filter_complex", ";".join(filters), "-map", f"[{prev}]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-r", str(FPS), "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print("wrote", out)


if __name__ == "__main__":
    root, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    for d in sorted(glob.glob(os.path.join(root, "*"))):
        build(d, os.path.join(out_dir, os.path.basename(d) + ".mp4"))
