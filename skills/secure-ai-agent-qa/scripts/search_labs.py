#!/usr/bin/env python3
"""Search supplied DLI course PDF pages or retrieve a precise module/page. Stdlib only."""
import argparse
import json
from pathlib import Path

from search_sources import norm, terms_for, excerpt

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?', default='')
    parser.add_argument('--module', type=int, help='0=course home; 1–10=supplied modules')
    parser.add_argument('--page', type=int, action='append', help='1-based PDF page; repeatable; requires --module')
    parser.add_argument('--limit', type=int, default=4)
    parser.add_argument('--full', action='store_true')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--links', action='store_true', help='Show external reading links on each matched page')
    args = parser.parse_args()
    rows = [json.loads(line) for line in (ROOT / 'references/corpus/labs-ko.jsonl').read_text(encoding='utf-8').splitlines() if line]
    if args.limit < 1:
        parser.error('--limit must be positive')
    if args.module is not None:
        if args.module not in {r['module'] for r in rows}:
            parser.error('No supplied PDF for this module. Available: 0 (home), 1–10. Modules 11–12 are not supplied.')
        rows = [r for r in rows if r['module'] == args.module]
    if args.page:
        if args.module is None:
            parser.error('--page requires --module')
        missing = set(args.page) - {r['page'] for r in rows}
        if missing:
            parser.error('No such PDF page: ' + ', '.join(map(str, sorted(missing))))
        found = [r for r in rows if r['page'] in args.page]
    elif args.query.strip():
        terms, phrase = terms_for(args.query), norm(args.query)
        ranked = []
        for row in rows:
            body, title = norm(row['text']), norm(row['title'])
            score = sum((4 if t in title else 0) + (2 if t in body else 0) for t in terms)
            if phrase in body:
                score += 10
            if phrase in title:
                score += 10
            if score:
                ranked.append((score, row))
        found = [r for _, r in sorted(ranked, key=lambda p: (-p[0], p[1]['module'], p[1]['page']))[:args.limit]]
    elif args.module is not None:
        found = rows
    else:
        parser.error('Provide query, --module, or --module with --page')
    if args.json:
        print(json.dumps(found, ensure_ascii=False, indent=2))
        return
    if not found:
        print('No matches. Read references/lab-modules.md or use fewer keywords.')
    for row in found:
        print(f"\n## Module {row['module']} · {row['title']} · PDF page {row['page']}")
        print(f"Source: {row['file']}; snapshot={row['snapshot_date']}; textbook, not a runtime observation")
        print(row['text'] if args.full else excerpt(row['text'], args.query, 1800))
        if args.links:
            print('\nExternal links (link presence alone does not mean reviewed):')
            print('\n'.join(row['external_links']) or '(none)')
        if not args.full:
            print('[Excerpt mode; use --full for complete page text. Images are not OCRed.]')


if __name__ == '__main__':
    main()
