#!/usr/bin/env python3
"""Extract supplied Korean course PDFs into a portable page corpus. Requires pymupdf."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
TITLES = {0: '과정 개요와 더 읽을거리', 1: 'Codex와 실습 환경', 2: '서브 에이전트와 팀',
          3: '인터페이스와 인젝션', 4: '자격 증명과 의존성', 5: '외부에서의 공격',
          6: '사용자로부터의 공격', 7: '내부에서의 공격', 8: 'OpenShell 격리',
          9: '런타임 보호', 10: '심층 방어'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=ROOT / 'references')
    args = parser.parse_args()
    try:
        import pymupdf
    except ImportError:
        parser.error('PDF refresh requires pymupdf; search_labs.py needs only Python stdlib.')
    records, sources, reading_links = [], [], {}
    files = sorted(args.input.glob('*.pdf'), key=lambda p: (not p.stem.isdigit(), int(p.stem) if p.stem.isdigit() else 0))
    if not files:
        parser.error('No PDF files found')
    # Read all PDFs before modifying an existing corpus.
    for path in files:
        module = int(path.stem) if path.stem.isdigit() else 0
        if module not in TITLES or (module == 0 and path.stem != 'Securing Agents · NVIDIA DLI'):
            parser.error(f'Unmapped course PDF: {path.name}; update TITLES before ingesting')
        with pymupdf.open(path) as document:
            for number, page in enumerate(document, 1):
                links = sorted({link['uri'] for link in page.get_links() if link.get('uri')})
                external = [url for url in links if urlsplit(url).hostname != '52.201.250.178']
                records.append(dict(source_id=f'dli-codex-{module}', module=module,
                                    title=TITLES[module], file=f'DLI_codex/{path.name}',
                                    page=number, text=page.get_text(), external_links=external,
                                    snapshot_date='2026-10-28', language='ko'))
                for url in external:
                    reading_links.setdefault(url, []).append(dict(module=module, page=number))
            sources.append(dict(id=f'dli-codex-{module}', kind='local-lab-pdf', file=f'DLI_codex/{path.name}',
                                title=TITLES[module], module=module, pages=len(document), language='ko',
                                sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                snapshot_date='2026-10-28', checked_date=datetime.date.today().isoformat(),
                                status='page-text-and-link-extraction', runtime_executed=False,
                                local_reference='corpus/labs-ko.jsonl',
                                scope='PDF 본문과 링크. 이미지 전용 내용은 OCR하지 않음. 실행 결과가 아닌 교재 사본.'))
    output = args.output
    (output / 'corpus').mkdir(parents=True, exist_ok=True)
    manifest_path = output / 'sources.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else []
    manifest = [s for s in manifest if not s['id'].startswith('dli-codex-')]
    (output / 'corpus/labs-ko.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in records), encoding='utf-8')
    manifest_path.write_text(json.dumps(manifest + sources, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    # Link presence is distinct from reviewing the linked source. The main manifest records reviews.
    (output / 'lab-reading-links.json').write_text(json.dumps([
        dict(url=url, cited_at=locations, status='link-extracted-not-necessarily-reviewed')
        for url, locations in sorted(reading_links.items())], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(files)} PDFs; {len(records)} pages; {len(reading_links)} distinct external reading links')


if __name__ == '__main__':
    main()
