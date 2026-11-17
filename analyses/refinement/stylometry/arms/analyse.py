#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Herhaalde armen-meting (RESULTS §12): volledige agent (A) vs kale variant (B) vs geen gids (C),
op twee modellen, met eigen premisse en 3 concepten per cel. Deterministisch, geen LLM-jury.

Eenheden. Elk concept en elk echt verhaal wordt identiek afgekapt op de eerste zinnen tot
>=400 woorden (lengte kan dus niets verklappen). Echte vergelijkingseenheden: de 46 losse
Tellegen-verhalen van >=400 woorden (stylometry/raw/gold_all_*.txt).

Maat 1 - afstand tot het corpus-profiel: MFW-Delta en char3-Delta uit het ONGEWIJZIGDE
  measure.py (hier geimporteerd). Per dier het gemiddelde over de 3 concepten.
Maat 2 - detecteerbaarheid: een twee-centroiden-Delta-classifier (echt vs arm), gekruist
  gevalideerd per dier; AUC 0,5 = niet te onderscheiden van echt, 1,0 = volledig te scheiden.
  Gebruikt richting van de afwijking, niet alleen de grootte, en verzadigt dus niet zodra
  een arm "binnen het echte bereik" valt. Diernamen zijn hier gemaskeerd (elke naam -> 'xx'),
  omdat eekhoorn/mier/krekel anders als kenmerk meetellen en de detector het dier zou
  herkennen in plaats van de stijl; eigen kenmerklijsten (100 woorden, 300 trigrammen) en
  standaardisatie op het gemaskeerde corpus. Maat 1 blijft ongemaskeerd (measure.py).

BESLISREGEL (vastgelegd voor de eerste generatie; daarna niet bijstellen)
  Primair, per model: A vs B op maat 1. Alleen een bevinding als A en B op BEIDE families
  in dezelfde richting verschillen met exacte gepaarde permutatietoets (tekenwissel over de
  12 dieren, tweezijdig) p<0,05. Alles daaronder: geen aantoonbaar verschil.
  Secundair (gerapporteerd, niet beslissend): AUC en d' (scheiding in sd-eenheden, verzadigt
  niet bij AUC ~1) per arm en het verschil A-B (permutatie van armlabels binnen dier); A vs C en B vs C; Opus vs Fable per arm;
  spreiding binnen een cel; 8-gram-overlap met het corpus; lengtes.
  Geen armen, maten of dieren erbij na het zien van resultaten.

Gebruik (vanuit analyses/refinement/):
  python3 stylometry/arms/analyse.py --controls    # instrument-check, heeft geen concepten nodig
  python3 stylometry/arms/analyse.py               # de meting
"""
import contextlib, glob, io, os, re, statistics as st, sys

sys.path.insert(0, 'stylometry')
_argv, sys.argv = sys.argv, sys.argv[:1]
with contextlib.redirect_stdout(io.StringIO()):
    import measure as M                            # het instrument, ongewijzigd
sys.argv = _argv

D = 'stylometry/arms'
SEEDS = ['eekhoorn', 'mier', 'krekel', 'olifant', 'egel', 'schildpad', 'beer', 'mossel', 'krab', 'mug', 'kreeft', 'leeuw']
MODELS = ['opus', 'fable']
ARMS = ['A', 'B', 'C']
FAMS = ['MFW', 'char3']
CUT = 400
SPLIT = re.compile(r'(?<=[.!?])\s+')


def head(text, n=CUT):
    """eerste zinnen tot >= n woorden; gooit niets weg"""
    out, k = [], 0
    for s in SPLIT.split(M.clean(text)):
        out.append(s); k += len(M.toks(s))
        if k >= n: break
    return ' '.join(out)


def zvec(text, fam):
    v, m, s = (M.mfwvec(text), M.mfw_m, M.mfw_s) if fam == 'MFW' else (M.cgvec(text), M.cg_m, M.cg_s)
    return [(v[i] - m[i]) / s[i] for i in range(len(v))]


SPEAK = re.compile(r"\b(?:zei|vroeg|riep|dacht|mompelde|fluisterde|antwoordde|zuchtte|schreeuwde|piepte|bromde|zeiden|vroegen|riepen|dachten)\s+(?:de|het)\s+([a-zàáâäèéêëìíîïòóôöùúûüçñ]{3,})(?=[.,!?:;'])")


class Detector:
    """kenmerkruimte met gemaskeerde diernamen; naam = woord dat minstens 2x als spreker optreedt
    ("zei de X." / "vroeg het X,") in corpus of concepten, plus de 12 opdracht-dieren"""
    def __init__(self, extra_texts=()):
        cnt = {}
        for t in [M.real] + [M.clean(x) for x in extra_texts]:
            for w in SPEAK.findall(t.lower()): cnt[w] = cnt.get(w, 0) + 1
        self.names = set(SEEDS) | {w for w, c in cnt.items() if c >= 2}
        self.rx = re.compile(r"\b(?:" + '|'.join(sorted(self.names, key=len, reverse=True)) + r")\b")
        wins = [self.mask(w) for w in M.samp]
        allm = ' '.join(wins)
        self.feat = {'MFW': self.top(M.toks(allm), 100), 'char3': self.top(M.cgr(allm), 300)}
        self.par = {f: M.zparams([self.vec(w, f, masked=True) for w in wins]) for f in FAMS}
    def mask(self, text): return self.rx.sub('xx', M.clean(text).lower())
    @staticmethod
    def top(items, k):
        c = {}
        for x in items: c[x] = c.get(x, 0) + 1
        return [x for x, _ in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:k]]
    def vec(self, text, fam, masked=False):
        t = text if masked else self.mask(text)
        u = M.toks(t) if fam == 'MFW' else M.cgr(t); n = len(u) or 1; c = {}
        for x in u: c[x] = c.get(x, 0) + 1
        return [c.get(f, 0) / n for f in self.feat[fam]]
    def z(self, text, fam):
        v = self.vec(text, fam); m, sd = self.par[fam]
        return [(v[i] - m[i]) / sd[i] for i in range(len(v))]


def centroid_dist(text):
    md, cd, comma, ttr = M.measure(text)
    return {'MFW': md, 'char3': cd, 'komma': comma, 'ttr': ttr}


def real_units(n=CUT):
    out = []
    for p in sorted(glob.glob('stylometry/raw/gold_all_*.txt')):
        t = M.load(p)
        if len(M.toks(t)) >= n: out.append(head(t, n))
    return out


# ---------- statistiek ----------
def signflip(diffs):
    """exacte tweezijdige gepaarde permutatietoets op het gemiddelde verschil"""
    n, obs, c = len(diffs), abs(sum(diffs)), 0
    for bits in range(1 << n):
        s = sum(d if bits >> i & 1 else -d for i, d in enumerate(diffs))
        c += abs(s) >= obs - 1e-12
    return c / (1 << n)


def l1(a, b): return sum(abs(x - y) for x, y in zip(a, b)) / len(a)
def vsum(vs): return [sum(c) for c in zip(*vs)]
def auc(pos, neg): return sum((p > q) + 0.5 * (p == q) for p in pos for q in neg) / (len(pos) * len(neg))


def prep_real(real_z, F):
    """per vouw: echt-centroide zonder de achtergehouden echte eenheden, en die eenheden met hun afstand"""
    tot, folds = vsum(real_z), []
    for f in range(F):
        held = [v for i, v in enumerate(real_z) if i % F == f]
        hs = vsum(held) if held else [0.0] * len(tot)
        cR = [(tot[i] - hs[i]) / (len(real_z) - len(held)) for i in range(len(tot))]
        folds.append((cR, [(v, l1(v, cR)) for v in held]))
    return folds


def prep_arm(groups, folds):
    """groups: per vouw de z-vectoren van de arm -> per vouw ([(vec, afstand tot echt)], somvector)"""
    return [([(v, l1(v, cR)) for v in g], vsum(g)) for g, (cR, _held) in zip(groups, folds)]


def cv_scores(folds, arm):
    tot = vsum([s for _items, s in arm]); na = sum(len(items) for items, _s in arm)
    pos, neg = [], []
    for (cR, held), (items, s) in zip(folds, arm):
        cX = [(tot[i] - s[i]) / (na - len(items)) for i in range(len(tot))]
        pos += [dR - l1(v, cX) for v, dR in items]       # hoger = lijkt meer op de arm dan op echt
        neg += [dR - l1(v, cX) for v, dR in held]
    return pos, neg


def cv_auc(folds, arm): return auc(*cv_scores(folds, arm))


def cv_dprime(folds, arm):
    """scheiding in sd-eenheden: (gem. score arm - gem. score echt) / gepoolde sd; 0 = geen scheiding"""
    pos, neg = cv_scores(folds, arm)
    sp = ((st.pvariance(pos) * len(pos) + st.pvariance(neg) * len(neg)) / (len(pos) + len(neg))) ** .5
    return (st.mean(pos) - st.mean(neg)) / sp if sp else 0.0


def diff_p(folds, x, y, stat):
    """exacte permutatie: wissel per vouw (dier) de concepten van arm x en y"""
    obs = stat(folds, x) - stat(folds, y); n = len(x); c = 0
    for bits in range(1 << n):
        px = [y[i] if bits >> i & 1 else x[i] for i in range(n)]
        py = [x[i] if bits >> i & 1 else y[i] for i in range(n)]
        c += abs(stat(folds, px) - stat(folds, py)) >= abs(obs) - 1e-12
    return obs, c / (1 << n)


# ---------- instrument-check ----------
def controls():
    print('=== instrument-check van de detector (geen nieuwe concepten nodig) ===')
    old = {'niet-constrained (bestofn+premise+thema)': sorted(glob.glob('stylometry/bestofn/*.txt')) + sorted(glob.glob('stylometry/ai_premise/*.txt')) + sorted(glob.glob('stylometry/ai_theme/*.txt')),
           'modellen §10 sonnet+haiku': sorted(glob.glob('stylometry/models/sonnet_*.txt')) + sorted(glob.glob('stylometry/models/haiku_*.txt')),
           'constrained §9 + opus 4.8 §10': sorted(glob.glob('stylometry/constrained/*.txt')) + sorted(glob.glob('stylometry/models/opus_*.txt'))}
    det = Detector([M.load(p) for ps in old.values() for p in ps])
    print(f'gemaskeerde namen ({len(det.names)}): {" ".join(sorted(det.names))}')
    print('MFW na maskering:', ' '.join(det.feat['MFW'][:40]), '...')
    for n in (CUT, 300):
        real = real_units(n)
        print(f'\nechte eenheden van >={n} woorden: {len(real)}')
        d = [centroid_dist(t) for t in real]
        for fam in FAMS:
            x = [r[fam] for r in d]
            print(f'  afstand tot profiel {fam:5s} (measure.py): gem {st.mean(x):.3f} sd {st.pstdev(x):.3f} bereik {min(x):.3f}-{max(x):.3f}')
        for fam in FAMS:                                 # echt vs echt, leave-one-out: verwacht AUC ~0,5
            res = []
            for off in (0, 1, 2):                        # drie verschillende splitsingen om de spreiding te zien
                rz = [det.z(t, fam) for t in real]; b = rz[off::3]; a = [v for i, v in enumerate(rz) if i % 3 != off]
                folds = prep_real(a, len(b)); arm = prep_arm([[v] for v in b], folds); res.append((cv_auc(folds, arm), cv_dprime(folds, arm)))
            print(f"  {fam:5s} echt vs echt (1/3 tegen 2/3, drie splitsingen): AUC " + ' '.join(f'{x:.3f}' for x, _ in res) + "  d' " + ' '.join(f'{y:+.2f}' for _, y in res))
    real = real_units(300)
    print('\noude AI-teksten uit de repo (afgekapt op >=300 woorden) tegen echt, leave-one-out:')
    for name, paths in old.items():
        texts = [head(M.load(p), 300) for p in paths]
        for fam in FAMS:
            folds = prep_real([det.z(t, fam) for t in real], len(texts))
            arm = prep_arm([[det.z(t, fam)] for t in texts], folds)
            print(f"  {fam:5s} echt vs {name:42s} (n={len(texts):2d}): AUC {cv_auc(folds, arm):.3f}  d' {cv_dprime(folds, arm):.2f}")


# ---------- de meting ----------
def load_drafts():
    dr = {}
    for m in MODELS:
        for a in ARMS:
            for s in SEEDS:
                dr[(m, a, s)] = [M.load(p) for p in sorted(glob.glob(f'{D}/drafts/{m}/{a}_{s}_*.txt'))]
    return dr


def overlap8(text, C8):
    t = re.findall(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]+", text.lower()); g = [tuple(t[i:i + 8]) for i in range(len(t) - 7)]
    return 100 * sum(x in C8 for x in g) / len(g) if g else 0.0


def main():
    dr = load_drafts()
    missing = [k for k, v in dr.items() if len(v) != 3]
    print(f'concepten: {sum(len(v) for v in dr.values())} van {len(dr) * 3}' + (f' | ONVOLLEDIGE cellen: {missing}' if missing else ''))
    real = real_units(); rd = [centroid_dist(t) for t in real]
    print(f'\n=== echte eenheden (n={len(real)}, eerste >={CUT} woorden) ===')
    for fam in FAMS:
        x = [r[fam] for r in rd]
        print(f'{fam:5s} afstand tot profiel: gem {st.mean(x):.3f} sd {st.pstdev(x):.3f} bereik {min(x):.3f}-{max(x):.3f}')
    det = Detector([t for texts in dr.values() for t in texts])
    print(f'detector: {len(det.names)} diernamen gemaskeerd')
    corpus = re.findall(r"[a-zàáâäèéêëìíîïòóôöùúûüçñ]+", M.real.lower()); C8 = {tuple(corpus[i:i + 8]) for i in range(len(corpus) - 7)}

    cell, rows = {}, []
    for (m, a, s), texts in dr.items():
        ms = []
        for i, raw in enumerate(texts, 1):
            h = head(raw); c = centroid_dist(h); c['woorden'] = len(M.toks(raw)); c['ov8'] = overlap8(raw, C8); c['dq'] = raw.count('"')
            ms.append(c); rows.append((m, a, s, i, c))
        cell[(m, a, s)] = ms
    with open(f'{D}/results.tsv', 'w', encoding='utf-8') as f:
        f.write('# model\tarm\tdier\tnr\twoorden\tMFW\tchar3\tkomma100\tTTR300\t8gram%\tdubbele_quotes\n')
        for m, a, s, i, c in rows:
            f.write(f"{m}\t{a}\t{s}\t{i}\t{c['woorden']}\t{c['MFW']:.3f}\t{c['char3']:.3f}\t{c['komma']:.1f}\t{c['ttr']:.2f}\t{c['ov8']:.1f}\t{c['dq']}\n")

    mean = lambda m, a, s, k: st.mean(c[k] for c in cell[(m, a, s)])
    for m in MODELS:
        print(f'\n=================== model: {m} ===================')
        print('%-4s %7s %7s %7s %6s %5s %6s %6s %s' % ('arm', 'MFW', 'char3', 'woorden', 'komma', 'TTR', 'ov8>0', 'dq>0', 'spreiding binnen cel (gem. sd) MFW / char3'))
        for a in ARMS:
            allc = [c for s in SEEDS for c in cell[(m, a, s)]]
            sd = {k: st.mean(st.stdev(c[k] for c in cell[(m, a, s)]) for s in SEEDS if len(cell[(m, a, s)]) > 1) for k in FAMS}
            print('%-4s %7.3f %7.3f %7.0f %6.1f %5.2f %6d %6d   %.3f / %.3f' % (a, st.mean(c['MFW'] for c in allc), st.mean(c['char3'] for c in allc),
                  st.mean(c['woorden'] for c in allc), st.mean(c['komma'] for c in allc), st.mean(c['ttr'] for c in allc),
                  sum(c['ov8'] > 0 for c in allc), sum(c['dq'] > 0 for c in allc), sd['MFW'], sd['char3']))
        print('\ngepaard per dier (gemiddelde van 3 concepten); verschil = eerste min tweede, negatief = eerste dichter bij Tellegen')
        for x, y in (('A', 'B'), ('A', 'C'), ('B', 'C')):
            out = []
            for fam in FAMS:
                diffs = [mean(m, x, s, fam) - mean(m, y, s, fam) for s in SEEDS]
                out.append(f'{fam} {st.mean(diffs):+.3f} ({x} dichter in {sum(d < 0 for d in diffs)}/12, p={signflip(diffs):.3f})')
            print(f'  {x} vs {y}: ' + ' | '.join(out) + ('   <- PRIMAIR' if (x, y) == ('A', 'B') else ''))
        print('\ndetecteerbaarheid (AUC echt vs arm, diernamen gemaskeerd; 0,5 = niet te onderscheiden)')
        for fam in FAMS:
            folds = prep_real([det.z(t, fam) for t in real], len(SEEDS))
            arms = {a: prep_arm([[det.z(head(t), fam) for t in dr[(m, a, s)]] for s in SEEDS], folds) for a in ARMS}
            for label, stat in (('AUC', cv_auc), ("d'", cv_dprime)):
                line = f'  {fam:5s} {label:3s} ' + '  '.join(f'{a} {stat(folds, arms[a]):.3f}' for a in ARMS)
                for x, y in (('A', 'B'), ('A', 'C'), ('B', 'C')):
                    dlt, p = diff_p(folds, arms[x], arms[y], stat); line += f' | {x}-{y} {dlt:+.3f} (p={p:.3f})'
                print(line)
    print('\n=================== Opus vs Fable, per arm (gepaard per dier; negatief = Fable dichter) ===================')
    for a in ARMS:
        out = []
        for fam in FAMS:
            diffs = [mean('fable', a, s, fam) - mean('opus', a, s, fam) for s in SEEDS]
            out.append(f'{fam} {st.mean(diffs):+.3f} (Fable dichter in {sum(d < 0 for d in diffs)}/12, p={signflip(diffs):.3f})')
        print(f'  arm {a}: ' + ' | '.join(out))


if __name__ == '__main__':
    controls() if '--controls' in sys.argv else main()
