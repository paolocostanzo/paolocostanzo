#!/usr/bin/env python3
"""Generate assets/htb-card.svg from the public Hack The Box profile API.

Compact self-hosted card: HTB navy and green with the HTB mark, Share Tech Mono +
Barlow Condensed embedded so it renders the same inside GitHub's <img> sandbox.
Refreshed every 6 hours by .github/workflows/htb-card.yml.
"""
LOGO = "m22.5106 6.4566.0008-.0123a.888.888 0 0 0-.2717-.6384c-.0084-.0084-.018-.0155-.0267-.0235-.0186-.0166-.0371-.0333-.0572-.0484-.0193-.0147-.04-.0276-.0607-.0406-.0096-.006-.0182-.0131-.0281-.0188L12.4576.1266a.891.891 0 0 0-.9223.0043L1.933 5.6744c-.0107.0062-.0203.014-.0307.0205-.0073.0047-.015.008-.0223.0128-.007.0047-.013.0106-.02.0155a.8769.8769 0 0 0-.147.1333l-.0026.003a.8872.8872 0 0 0-.2218.5847l.0009.014c-.0002.0088-.0015.0176-.0015.0264v11.0708c0 .3277.1802.6288.469.7836l9.5986 5.5417c.0076.0044.0158.0075.0236.0117a.8754.8754 0 0 0 .166.0687c.0134.004.0266.0083.0401.0117a.8793.8793 0 0 0 .072.0142c.0117.0019.0232.0045.0349.006a.835.835 0 0 0 .2157 0c.0117-.0015.0232-.0041.0348-.006a.9.9 0 0 0 .072-.0142c.0135-.0034.0267-.0077.04-.0117a.895.895 0 0 0 .0646-.0217.9134.9134 0 0 0 .1015-.047c.0078-.0042.016-.0072.0236-.0117l9.5986-5.5417a.8888.8888 0 0 0 .469-.7836V6.4779c0-.0071-.0012-.0142-.0014-.0213zM5.2543 6.0822l6.5367-3.774a.4182.4182 0 0 1 .4182 0l6.5366 3.774a.4182.4182 0 0 1 0 .7243l-6.5367 3.774a.4182.4182 0 0 1-.4182 0l-6.5366-3.774a.4182.4182 0 0 1 0-.7243zm5.6134 14.3449a.4172.4172 0 0 1-.626.3613L3.718 17.0218a.4173.4173 0 0 1-.2086-.3613V9.1279a.4172.4172 0 0 1 .6258-.3613l6.524 3.7666a.4172.4172 0 0 1 .2086.3614v7.5325zm9.623-3.7666a.4173.4173 0 0 1-.2086.3613l-6.5239 3.7666a.4172.4172 0 0 1-.6259-.3613v-7.5325c0-.149.0796-.2868.2087-.3614l6.5239-3.7666a.4172.4172 0 0 1 .6258.3613v7.5326z"  # Simple Icons (CC0), Hack The Box mark

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

    svg = f'''<svg width="300" height="50" viewBox="0 0 300 50" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Hack The Box: {rank}, global rank #{ranking}">
<title>Hack The Box: {rank}, global rank #{ranking}</title>
<style>
@font-face{{font-family:'STM';src:url(data:font/woff2;base64,{mono}) format('woff2');}}
@font-face{{font-family:'BC';src:url(data:font/woff2;base64,{cond}) format('woff2');}}
.m{{font-family:'STM','Share Tech Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;}}
.c{{font-family:'BC','Barlow Condensed','Arial Narrow',sans-serif;font-weight:900;}}
</style>
<rect x="0.5" y="0.5" width="299" height="49" rx="8" fill="#141D2B" stroke="#24344A"/>
<g transform="translate(13 13) scale(1)"><path fill="#9FEF00" d="{LOGO}"/></g>
<text x="47" y="21" class="m" font-size="10" fill="#8A97A8" letter-spacing="1">HACK THE BOX</text>
<text x="46" y="39" class="c" font-size="19" fill="#E8EDF3" letter-spacing="0.4">{rank}</text>
<line x1="200" y1="11" x2="200" y2="39" stroke="#24344A"/>
<text x="286" y="21" class="m" font-size="10" fill="#8A97A8" text-anchor="end" letter-spacing="1">GLOBAL</text>
<text x="286" y="40" class="c" font-size="21" fill="#9FEF00" text-anchor="end">#{ranking}</text>
</svg>
'''
    OUT.write_text(svg)
    print(f"wrote {OUT} ({rank}, #{ranking}, {challenges} ch, {machines} m)")


if __name__ == "__main__":
    main()
