#!/usr/bin/env python3
"""Generate assets/htb-card.svg from the public Hack The Box profile API.

Self-hosted card in the style of paolocostanzo.github.io (dark, #FF6A00,
Share Tech Mono + Barlow Condensed, fonts embedded so it renders the same
inside GitHub's <img> sandbox). Run daily by .github/workflows/htb-card.yml.
"""
import base64, datetime, html, json, pathlib, sys, urllib.request

USER_ID = 2960827
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "htb-card.svg"
API = "https://labs.hackthebox.com/api/v4"


def get(path):
    req = urllib.request.Request(f"{API}/{path}", headers={
        "User-Agent": "paolocostanzo-readme-card", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def font(name):
    data = (ROOT / "assets" / "fonts" / f"{name}.woff2").read_bytes()
    return base64.b64encode(data).decode()


def main():
    p = get(f"profile/{USER_ID}")["profile"]
    ch = get(f"profile/progress/challenges/{USER_ID}")["profile"]["challenge_owns"]
    rank = html.escape(str(p["rank"]).upper())
    ranking = p.get("ranking")
    if not ranking:
        sys.exit("no global ranking in API response, keeping the previous card")
    machines = p.get("system_owns", 0)
    challenges = ch.get("solved", 0)
    today = datetime.date.today().isoformat()
    mono = font("share-tech-mono-latin-400-normal")
    cond = font("barlow-condensed-latin-900-normal")

    svg = f'''<svg width="480" height="132" viewBox="0 0 480 132" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Hack The Box: {rank}, global rank #{ranking}">
<title>Hack The Box: {rank}, global rank #{ranking}</title>
<style>
@font-face{{font-family:'STM';src:url(data:font/woff2;base64,{mono}) format('woff2');}}
@font-face{{font-family:'BC';src:url(data:font/woff2;base64,{cond}) format('woff2');}}
.m{{font-family:'STM','Share Tech Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;}}
.c{{font-family:'BC','Barlow Condensed','Arial Narrow',sans-serif;font-weight:900;}}
</style>
<defs><clipPath id="r"><rect x="0" y="0" width="480" height="132" rx="10"/></clipPath></defs>
<g clip-path="url(#r)"><rect width="480" height="132" fill="#161616"/><rect width="5" height="132" fill="#FF6A00"/></g>
<rect x="0.5" y="0.5" width="479" height="131" rx="10" fill="none" stroke="#2a2a2a"/>
<text x="24" y="30" class="m" font-size="12" fill="#888888" letter-spacing="1">HACK THE BOX <tspan fill="#FF6A00">//</tspan> paolocostanzo</text>
<text x="22" y="76" class="c" font-size="40" fill="#E8E8E8" letter-spacing="0.5">{rank}</text>
<text x="456" y="72" class="c" font-size="44" fill="#FF6A00" text-anchor="end">#{ranking}</text>
<text x="456" y="30" class="m" font-size="12" fill="#888888" text-anchor="end" letter-spacing="1">GLOBAL RANK</text>
<line x1="24" y1="94" x2="456" y2="94" stroke="#2a2a2a"/>
<text x="24" y="116" class="m" font-size="13" fill="#E8E8E8"><tspan fill="#FFAA00">{challenges}</tspan> challenges <tspan fill="#4a4a4a">·</tspan> <tspan fill="#FFAA00">{machines}</tspan> machines</text>
<text x="456" y="116" class="m" font-size="11" fill="#4a4a4a" text-anchor="end">updated {today}</text>
</svg>
'''
    OUT.write_text(svg)
    print(f"wrote {OUT} ({rank}, #{ranking}, {challenges} ch, {machines} m)")


if __name__ == "__main__":
    main()
