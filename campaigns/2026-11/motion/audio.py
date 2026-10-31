"""Original soundtrack + haptic sound design for NNWA motion reels (all synthesised here, so no licensing).

python3 audio.py <events.json> <duration-seconds> <out.wav> [key]
Music: upbeat 120 BPM house-pop loop (four-on-the-floor kick, claps, offbeat hats, sidechained bass,
syncopated chord plucks, bell arpeggio), I-V-vi-IV in the given key. SFX: soft UI ticks per word,
whoosh + impact per transition, counter clicks, pops, sparkles, typing keys, chime on the end card.
"""
import json
import sys

import numpy as np
from scipy.signal import butter, lfilter, sosfilt

SR = 44100
BPM = 120
BEAT = 60 / BPM
rng = np.random.default_rng(11)

KEYS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9}


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def t_arr(dur):
    return np.arange(int(dur * SR)) / SR


def lp(x, f, order=2):
    return sosfilt(butter(order, min(f, SR / 2 - 100) / (SR / 2), "low", output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f / (SR / 2), "high", output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo / (SR / 2), min(hi, SR / 2 - 100) / (SR / 2)], "band", output="sos"), x)


def add(buf, sig, at, gain=1.0):
    i = int(at * SR)
    if i >= len(buf) or i + len(sig) <= 0:
        return
    j = min(len(buf), i + len(sig))
    s0 = max(0, -i)
    buf[max(i, 0):j] += gain * sig[s0:s0 + j - max(i, 0)]


def saw(f, dur, harm=24, detune=0.0):
    t = t_arr(dur)
    out = np.zeros_like(t)
    n = int(min(harm, (SR / 2) / (f * (1 + detune)) - 1))
    for k in range(1, max(n, 1) + 1):
        out += np.sin(2 * np.pi * k * f * (1 + detune) * t) / k
    return out * 0.6


# ---------------- instruments ----------------
def kick():
    t = t_arr(0.45)
    f = 48 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 7.5)
    click = hp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 300) * 0.25
    return np.tanh((body + click) * 1.6)


def clap():
    t = t_arr(0.35)
    n = rng.standard_normal(len(t))
    env = np.zeros_like(t)
    for d in (0, 0.011, 0.022):
        env += (t >= d) * np.exp(-np.clip(t - d, 0, None) * (60 if d < 0.02 else 18))
    return bp(n, 900, 5000) * env * 0.55


def hat(open_=False):
    t = t_arr(0.22 if open_ else 0.05)
    return hp(rng.standard_normal(len(t)), 7500) * np.exp(-t * (18 if open_ else 90)) * (0.28 if open_ else 0.18)


def pluck(freqs, dur=0.32, bright=4200):
    out = sum(saw(f, dur, 30, d) + saw(f, dur, 30, -d) for f in freqs for d in (0.004,))
    t = t_arr(dur)
    env = np.exp(-t * 9) * (1 - np.exp(-t * 400))
    return lp(out, bright) * env * 0.16


def pad(freqs, dur):
    out = sum(saw(f, dur, 12, d) for f in freqs for d in (-0.006, 0.0, 0.006))
    t = t_arr(dur)
    env = np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.4)
    return lp(out, 1400) * env * 0.035


def bass(f, dur=0.22):
    t = t_arr(dur)
    s = np.sin(2 * np.pi * f * t) + 0.35 * lp(saw(f, dur, 10), 600)
    return s * np.exp(-t * 6) * (1 - np.exp(-t * 300)) * 0.5


def bell(f, dur=0.5):
    t = t_arr(dur)
    s = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 10) + 0.2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 20)
    return s * np.exp(-t * 7) * 0.08


def reverb(x, mix=0.18):
    out = np.zeros_like(x)
    for d, g in ((1557, .84), (1617, .83), (1491, .82), (1422, .81), (1277, .8), (1356, .79)):
        a = np.zeros(d + 1); a[0] = 1; a[d] = -g
        out += lfilter([1], a, x)
    out /= 6
    for d in (225, 556, 441):
        b = np.zeros(d + 1); b[0] = -0.5; b[d] = 1
        a = np.zeros(d + 1); a[0] = 1; a[d] = -0.5
        out = lfilter(b, a, out)
    return x + mix * lp(out, 5000)


def music(dur, key="C"):
    n = int(dur * SR)
    drums, inst, bassb = np.zeros(n), np.zeros(n), np.zeros(n)
    root = 48 + KEYS.get(key, 0)  # C3
    prog = [[0, 4, 7, 11], [7, 11, 14, 17], [9, 12, 16, 19], [5, 9, 12, 16]]  # Imaj7  V(add) vi7  IV
    bass_root = [0, 7, 9, 5]
    K, C, HC, HO = kick(), clap(), hat(), hat(True)
    beats = int(dur / BEAT) + 1
    stabs = [0, 3, 6, 10, 12, 14]  # 16th positions in a bar: syncopated
    arp = [0, 2, 4, 7, 9, 12, 9, 7]  # major pentatonic run
    for b in range(beats):
        t = b * BEAT
        bar = b // 4
        ch = prog[bar % 4]
        add(drums, K, t, 0.95)
        if b % 2 == 1:
            add(drums, C, t, 0.8)
        add(drums, HO, t + BEAT / 2, 0.9)
        for s16 in (1, 3):
            add(drums, HC, t + s16 * BEAT / 4, 0.7)
        add(bassb, bass(midi(root - 12 + bass_root[bar % 4])), t + BEAT / 2, 1.0)
        if b % 4 == 0:
            for s in stabs:
                add(inst, pluck([midi(root + 12 + x) for x in ch[:3]]), t + s * BEAT / 4, 1.0)
            add(inst, pad([midi(root + x) for x in ch], 4 * BEAT + 0.3), t, 1.0)
        if bar % 2 == 1:  # bell arpeggio every other bar
            for k in range(2):
                add(inst, bell(midi(root + 24 + arp[(b * 2 + k) % 8])), t + k * BEAT / 2, 1.0)
    # sidechain pump from the kick
    tt = np.arange(n) / SR
    duck = 1 - 0.65 * np.exp(-(tt % BEAT) / 0.11)
    mix = drums + (inst + bassb) * duck
    mix = reverb(mix, 0.12)
    # end: last 1.2 s strip drums, fade
    fade = np.clip((dur - tt) / 1.2, 0, 1)
    return hp(mix, 30) * fade


# ---------------- sound design ----------------
def sfx(ev, dur):
    n = int(dur * SR)
    out = np.zeros(n)

    def tone(f0, f1, d, decay, gain, shape=np.sin):
        t = t_arr(d)
        f = f1 + (f0 - f1) * np.exp(-t * 30)
        return shape(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * decay) * gain

    for e in ev:
        t, ty, v = e["t"], e["type"], e.get("v", 0)
        if ty == "tick":  # haptic: low tock + soft click
            s = tone(220 + 8 * (v % 5), 160, 0.06, 70, 0.35)
            c = hp(rng.standard_normal(int(0.01 * SR)), 4000) * np.exp(-t_arr(0.01) * 500) * 0.12
            add(out, s, t); add(out, c, t)
        elif ty == "count":
            add(out, tone(1800 + 60 * v, 1500 + 60 * v, 0.025, 160, 0.10), t)
        elif ty == "pop":
            add(out, tone(500 + 120 * v, 950 + 120 * v, 0.12, 30, 0.35), t)
        elif ty == "land":  # number lands: thump + bright ping
            add(out, tone(140, 60, 0.25, 18, 0.6), t)
            add(out, bell(midi(88), 0.6) * 3.0, t)
        elif ty == "sparkle":
            for k, m in enumerate((96, 100, 103, 108)):
                add(out, bell(midi(m), 0.35) * 1.6, t + k * 0.035)
        elif ty == "whoosh":
            d = 0.62
            tt = t_arr(d)
            nz = rng.standard_normal(len(tt))
            env = np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 2
            lo = bp(nz, 300, 2500) * env
            hi = hp(nz, 3000) * env ** 3
            add(out, (lo * 0.45 + hi * 0.25), t)
        elif ty == "impact":
            add(out, tone(110, 40, 0.5, 9, 0.55), t)
            add(out, lp(rng.standard_normal(int(0.2 * SR)), 1800) * np.exp(-t_arr(0.2) * 25) * 0.25, t)
        elif ty == "hit":
            add(out, tone(120, 45, 0.7, 6, 0.6), t)
        elif ty == "thock":  # wood-block haptic for list items
            add(out, tone(420, 380, 0.08, 55, 0.4) + tone(840, 800, 0.08, 80, 0.15), t)
        elif ty == "check":
            add(out, tone(1200, 1600, 0.07, 45, 0.18), t)
        elif ty == "rise":
            tt = t_arr(1.1)
            f = 300 + 900 * (tt / 1.1) ** 2
            add(out, np.sin(2 * np.pi * np.cumsum(f) / SR) * (tt / 1.1) * 0.12 + bp(rng.standard_normal(len(tt)), 2000, 6000) * (tt / 1.1) ** 2 * 0.1, t)
        elif ty == "soft":
            tt = t_arr(0.3)
            add(out, bp(rng.standard_normal(len(tt)), 2500, 8000) * np.sin(np.pi * tt / 0.3) * 0.08, t)
        elif ty == "key":
            c = hp(rng.standard_normal(int(0.03 * SR)), 2000) * np.exp(-t_arr(0.03) * 180) * 0.3
            add(out, c + tone(900 + 30 * v, 700, 0.03, 120, 0.12), t)
        elif ty == "swish":
            tt = t_arr(0.35)
            add(out, hp(rng.standard_normal(len(tt)), 4000) * np.sin(np.pi * tt / 0.35) ** 2 * 0.25, t)
        elif ty == "chime":
            for k, m in enumerate((84, 88, 91, 96)):
                add(out, bell(midi(m), 1.6) * 2.2, t + k * 0.06)
    return reverb(out, 0.2)


def main():
    ev = json.load(open(sys.argv[1]))
    dur = float(sys.argv[2])
    key = sys.argv[4] if len(sys.argv) > 4 else "C"
    m = music(dur, key)
    s = sfx(ev, dur)
    mix = 0.55 * m / (np.max(np.abs(m)) + 1e-9) + 0.5 * s / (np.max(np.abs(s)) + 1e-9)
    mix = np.tanh(mix * 1.4) / np.tanh(1.4)
    mix *= 0.95 / (np.max(np.abs(mix)) + 1e-9)
    # light stereo: haas-delayed copy of the reverb-ish tail on the right
    left = mix
    right = np.concatenate([np.zeros(int(0.012 * SR)), mix])[:len(mix)] * 0.35 + mix * 0.65
    pcm = (np.stack([left, right], 1) * 32767).astype(np.int16)
    import wave
    with wave.open(sys.argv[3], "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print("wrote", sys.argv[3], f"{dur:.2f}s", len(ev), "events")


if __name__ == "__main__":
    main()
