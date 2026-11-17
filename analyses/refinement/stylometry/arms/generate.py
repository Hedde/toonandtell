#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schrijft de concepten voor de herhaalde armen-meting (RESULTS §12).

  12 dieren x 3 armen x 2 modellen x 3 herhalingen = 216 concepten, elk in een verse,
  geisoleerde context (claude -p --safe-mode, geen tools, lege werkmap).
  arm A = volledige schrijfagent (body van .claude/agents/toon-tellegen-schrijver.md);
  arm B = kale variant (de drie secties, identiek aan triad/arm_B_system.md);
  arm C = geen gids (system prompt: alleen "Je bent een schrijfagent.").
  Zelfde user-bericht voor alle armen (task_template.txt): alleen het dier, de doellengte en
  de opmaakregels. De premisse bedenkt de schrijver zelf.

Geen lengtepoort, geen review, geen selectie: elk concept telt zoals het komt. Een bestaand
concept wordt nooit overschreven; opnieuw draaien vult alleen ontbrekende cellen aan (na een
API-fout). Lengte wordt in de analyse gelijkgetrokken door afkappen op de eerste >=400 woorden.

Gebruik (vanuit analyses/refinement/):  python3 stylometry/arms/generate.py [logmap] [--limit N]
"""
import json, os, re, subprocess, sys, tempfile, threading, time
from concurrent.futures import ThreadPoolExecutor

D = 'stylometry/arms'
AGENT = '../../.claude/agents/toon-tellegen-schrijver.md'
SEEDS = ['eekhoorn', 'mier', 'krekel', 'olifant', 'egel', 'schildpad', 'beer', 'mossel', 'krab', 'mug', 'kreeft', 'leeuw']
MODELS = ['opus', 'fable']
REPS = 3
args = [a for a in sys.argv[1:] if not a.startswith('--')]
LOGDIR = args[0] if args else tempfile.mkdtemp(prefix='arms_log_')
LIMIT = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else None
WORD = re.compile(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]+(?:'[a-z]+)?")
lock = threading.Lock()


def systems():
    body = open(AGENT, encoding='utf-8').read().split('\n---\n', 1)[1].lstrip('\n')
    lines = body.split('\n')
    a = next(i for i, l in enumerate(lines) if l.startswith('# De motor: premisse-eerst'))
    b = next(i for i, l in enumerate(lines) if l.startswith('# Werkhiërarchie'))
    bare = '\n'.join(lines[a:b]).rstrip('\n') + '\n'
    assert bare == open('stylometry/triad/arm_B_system.md', encoding='utf-8').read()
    return {'A': body, 'B': bare, 'C': 'Je bent een schrijfagent.'}


def call(model, system, user, tag):
    for attempt, wait in enumerate((0, 60, 180, 420)):
        time.sleep(wait)
        with tempfile.TemporaryDirectory(prefix='arms_ctx_') as empty:
            p = subprocess.run(
                ['claude', '-p', '--safe-mode', '--model', model, '--system-prompt', system,
                 '--tools', '', '--strict-mcp-config', '--disable-slash-commands',
                 '--no-session-persistence', '--output-format', 'json'],
                input=user, capture_output=True, text=True, cwd=empty, timeout=1200)
        open(f'{LOGDIR}/{tag}_call{attempt}.json', 'w', encoding='utf-8').write(p.stdout or p.stderr)
        try:
            res = next(e for e in json.loads(p.stdout) if e.get('type') == 'result')
        except Exception:
            continue                                         # technische fout: opnieuw
        if res.get('is_error') or not (res.get('result') or '').strip():
            continue
        return res['result'].strip() + '\n', ','.join(res.get('modelUsage', {}).keys()), res.get('usage', {}).get('output_tokens', 0)
    return None


def job(j):
    model, arm, seed, rep, system, user = j
    path = f'{D}/drafts/{model}/{arm}_{seed}_{rep}.txt'
    if os.path.exists(path):
        return 'bestond al'
    out = call(model, system, user, f'{model}_{arm}_{seed}_{rep}')
    if out is None:
        return 'MISLUKT'
    text, model_id, tokens = out
    with lock:
        if os.path.exists(path):
            return 'bestond al'
        open(path, 'w', encoding='utf-8').write(text)
        with open(f'{D}/generation_log.tsv', 'a', encoding='utf-8') as f:
            f.write(f'{model}\t{arm}\t{seed}\t{rep}\t{len(WORD.findall(text.lower()))}\t{model_id}\t{tokens}\n')
    return 'geschreven'


def main():
    os.makedirs(LOGDIR, exist_ok=True)
    for m in MODELS: os.makedirs(f'{D}/drafts/{m}', exist_ok=True)
    if not os.path.exists(f'{D}/generation_log.tsv'):
        open(f'{D}/generation_log.tsv', 'w', encoding='utf-8').write('# model\tarm\tdier\tnr\twoorden\tmodel-id\toutput_tokens\n')
    sysm = systems(); template = open(f'{D}/task_template.txt', encoding='utf-8').read()
    jobs = [(m, a, s, r, sysm[a], template.format(DIER=s))
            for r in range(1, REPS + 1) for s in SEEDS for a in 'ABC' for m in MODELS]
    if LIMIT: jobs = jobs[:LIMIT]
    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(job, jobs))
    print({k: res.count(k) for k in sorted(set(res))}, '| log in', LOGDIR)


if __name__ == '__main__':
    main()
