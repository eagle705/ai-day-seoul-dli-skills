#!/usr/bin/env python3
"""Search slide text and speaker notes, or retrieve exact slides. Stdlib only."""
import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALIASES = [
    ('하네스', 'harness'), ('가드레일', 'guardrails', 'guardrail'),
    ('샌드박스', 'sandbox', '격리', 'containment'), ('삼요소', 'trifecta'),
    ('권한', 'privilege', 'permission', 'authority'),
    ('자격 증명', 'credential', 'credentials'), ('의존성', 'dependency', 'dependencies'),
    ('서명', 'signature', 'signed', 'hmac'), ('메모리', 'memory'),
    ('테인트', 'taint'), ('거버넌스', 'governance'),
    ('정형 검증', 'formal verification'), ('인젝션', 'injection'),
    ('유출', 'exfiltration'), ('평가', 'assessment', 'examiner'),
    ('런타임', 'runtime'), ('하드닝', 'hardening'), ('접근 통제', 'access control'),
    ('서브 에이전트', 'subagent', 'sub-agent'), ('카나리', 'canary'),
]


def norm(text):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', text).casefold()).strip()


def terms_for(query):
    raw = norm(query)
    terms = set(re.findall(r'[\w-]+', raw))
    for group in ALIASES:
        if any(norm(term) in raw for term in group):
            terms.update(norm(term) for term in group)
    return terms


def search(rows, query):
    terms = terms_for(query)
    phrase = norm(query)
    ranked = []
    for row in rows:
        title, body, notes = (norm(row[k]) for k in ('title', 'text', 'notes'))
        score = sum((5 if t in title else 0) + (3 if t in body else 0)
                    + (1 if t in notes else 0) for t in terms)
        if phrase and phrase in title:
            score += 20
        if score:
            ranked.append((score, row))
    return sorted(ranked, key=lambda p: (-p[0], p[1]['deck'] != 'seoul', p[1]['slide']))


def excerpt(text, query, size):
    if len(text) <= size:
        return text
    hits = [text.casefold().find(t) for t in terms_for(query)]
    start = max(0, min((h for h in hits if h >= 0), default=0) - 120)
    return ('…' if start else '') + text[start:start + size] + ('…' if start + size < len(text) else '')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('query', nargs='?', default='')
    p.add_argument('--deck', choices=['seoul', 'berlin', 'all'], default='all')
    p.add_argument('--slide', type=int, action='append', help='1-based exact slide; repeatable')
    p.add_argument('--limit', type=int, default=5)
    p.add_argument('--full', action='store_true', help='Print full text and notes')
    p.add_argument('--json', action='store_true', help='Return complete matched records as JSON')
    args = p.parse_args()
    if args.limit < 1:
        p.error('--limit must be positive')
    rows = []
    for deck in (['seoul', 'berlin'] if args.deck == 'all' else [args.deck]):
        path = ROOT / 'references' / 'corpus' / (deck + '.jsonl')
        rows.extend(json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line)
    if args.slide:
        found = [r for r in rows if r['slide'] in args.slide]
        missing = set(args.slide) - {r['slide'] for r in found}
        if missing:
            p.error('No such slide in selected deck(s): ' + ', '.join(map(str, sorted(missing))))
    elif args.query.strip():
        found = [r for _, r in search(rows, args.query)[:args.limit]]
    else:
        p.error('Provide a query or --slide')
    if args.json:
        print(json.dumps(found, ensure_ascii=False, indent=2))
        return
    if not found:
        print('No matches. Use fewer keywords or consult references/topic-map.md.')
    for row in found:
        print(f"\n## {row['deck']} slide {row['slide']} — {row['title']}")
        print(f"Source: {row['file']}; hidden={row['hidden']}")
        for key, label in [('text', 'Slide text'), ('notes', 'Speaker notes')]:
            content = row[key] or '(none)'
            print(f'\n### {label}\n' + (content if args.full else excerpt(content, args.query, 1600)))
        if not args.full:
            print('\n[Excerpt mode. Use --full to read complete evidence.]')


if __name__ == '__main__':
    main()
