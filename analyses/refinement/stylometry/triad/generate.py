#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schrijft per inhoudsbrief twee concepten in verse, geisoleerde contexten (RESULTS §11).

  arm A = de volledige schrijfagent: de body van .claude/agents/toon-tellegen-schrijver.md
          (alles na de frontmatter) als system prompt;
  arm B = kale variant: alleen de secties "De motor: premisse-eerst", "Temporeel register"
          en "Stylometrische register-constraints" uit DEZELFDE prompt (mechanisch uitgesneden,
          zie arm_B_system.md) als system prompt.

Beide armen: zelfde model (frontmatter van de agent: opus), zelfde user-bericht
(task_template.txt + brief), geen tools, geen CLAUDE.md/skills/geheugen (--safe-mode),
werkmap = lege tijdelijke map. Geen review-loop, geen surgery, geen selectie op kwaliteit.

Lengtepoort (vooraf vastgelegd, kijkt alleen naar het woordtal): een concept buiten
+/-15% van het gold-woordtal wordt ongemeten opzijgezet in rejected/ en opnieuw
geschreven uit dezelfde brief in een nieuwe context, hooguit 3 pogingen; de eerste
poging binnen de marge telt. Alles staat in generation_log.tsv.

Gebruik (vanuit analyses/refinement/):  python3 stylometry/triad/generate.py [logmap]
"""
import json, os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor

T = 'stylometry/triad'
AGENT = '../../.claude/agents/toon-tellegen-schrijver.md'
LOGDIR = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix='triad_log_')
MAXTRY = 3
WORD = re.compile(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]+(?:'[a-z]+)?")   # zelfde tokenisatie als measure.py


def nwords(t):
    for k, v in {'‘': "'", '’': "'"}.items():
        t = t.replace(k, v)
    return len(WORD.findall(t.lower()))


def systems():
    raw = open(AGENT, encoding='utf-8').read()
    body = raw.split('\n---\n', 1)[1].lstrip('\n')            # A: alles na de frontmatter
    lines = body.split('\n')
    start = next(i for i, l in enumerate(lines) if l.startswith('# De motor: premisse-eerst'))
    end = next(i for i, l in enumerate(lines) if l.startswith('# Werkhiërarchie'))
    bare = '\n'.join(lines[start:end]).rstrip('\n') + '\n'     # B: drie aaneengesloten secties
    heads = [l for l in bare.split('\n') if l.startswith('# ')]
    assert len(heads) == 3, heads
    open(f'{T}/arm_B_system.md', 'w', encoding='utf-8').write(bare)
    return {'A': body, 'B': bare}


def call(system, user, tag):
    with tempfile.TemporaryDirectory(prefix='triad_ctx_') as empty:
        p = subprocess.run(
            ['claude', '-p', '--safe-mode', '--model', 'opus', '--system-prompt', system,
             '--tools', '', '--strict-mcp-config', '--disable-slash-commands',
             '--no-session-persistence', '--output-format', 'json'],
            input=user, capture_output=True, text=True, cwd=empty, timeout=900)
    open(f'{LOGDIR}/{tag}.json', 'w', encoding='utf-8').write(p.stdout)
    events = json.loads(p.stdout)
    res = next(e for e in events if e.get('type') == 'result')
    if res.get('is_error'):
        raise RuntimeError(f'{tag}: {res.get("result")}')
    model = ','.join(res.get('modelUsage', {}).keys())
    return res['result'].strip() + '\n', model, res.get('usage', {}).get('output_tokens', 0)


def job(args):
    nr, arm, system, n, brief, template = args
    lo, hi = round(0.85 * n), round(1.15 * n)
    user = template.format(N=n, LO=round(0.9 * n), HI=round(1.1 * n), BRIEF=brief)
    rows = []
    for attempt in range(1, MAXTRY + 1):
        text, model, out = call(system, user, f'{arm}_{nr}_try{attempt}')
        w = nwords(text)
        ok = lo <= w <= hi
        rows.append((nr, arm, attempt, n, w, f'{100 * (w - n) / n:+.1f}', 'ja' if ok else 'nee', model, out))
        if ok or attempt == MAXTRY:
            open(f'{T}/{arm}_{nr}.txt', 'w', encoding='utf-8').write(text)
            break
        os.makedirs(f'{T}/rejected', exist_ok=True)
        open(f'{T}/rejected/{arm}_{nr}_try{attempt}.txt', 'w', encoding='utf-8').write(text)
    return rows


def main():
    os.makedirs(LOGDIR, exist_ok=True)
    sysm = systems()
    template = open(f'{T}/task_template.txt', encoding='utf-8').read()
    gold = [l.rstrip('\n').split('\t') for l in open(f'{T}/gold.tsv', encoding='utf-8') if not l.startswith('#')]
    jobs = []
    for nr, _bundle, _pages, words, _path in gold:
        brief = open(f'{T}/briefs/brief_{nr}.md', encoding='utf-8').read().strip()
        for arm in ('A', 'B'):
            jobs.append((nr, arm, sysm[arm], int(words), brief, template))
    with ThreadPoolExecutor(max_workers=6) as ex:
        rows = [r for rs in ex.map(job, jobs) for r in rs]
    rows.sort()
    with open(f'{T}/generation_log.tsv', 'w', encoding='utf-8') as f:
        f.write('# nr\tarm\tpoging\tgold_woorden\tconcept_woorden\tafwijking_%\tbinnen_15%\tmodel\toutput_tokens\n')
        for r in rows:
            f.write('\t'.join(str(x) for x in r) + '\n')
    with open(f'{T}/manifest.tsv', 'w', encoding='utf-8') as f:
        f.write('# gold\tconcept A (volledige agent)\tconcept B (kale variant)\n')
        for nr, _b, _p, _w, path in gold:
            f.write(f'{path}\t{T}/A_{nr}.txt\t{T}/B_{nr}.txt\n')
    print(f'{len(rows)} aanroepen, {sum(r[6] == "nee" for r in rows)} buiten de lengtemarge; log in {LOGDIR}')


if __name__ == '__main__':
    main()
