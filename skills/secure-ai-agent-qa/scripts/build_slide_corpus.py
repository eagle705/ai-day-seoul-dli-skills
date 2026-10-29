#!/usr/bin/env python3
"""Refresh the bundled slide corpus from the two supplied PPTX files (stdlib only)."""
import argparse
import datetime
import hashlib
import json
import posixpath
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
ROOT = Path(__file__).resolve().parents[1]


def relationships(archive, part):
    directory, filename = posixpath.split(part)
    rel = posixpath.join(directory, '_rels', filename + '.rels')
    if rel not in archive.namelist():
        return {}
    result = {}
    for element in ET.fromstring(archive.read(rel)):
        data = dict(element.attrib)
        if data.get('TargetMode') != 'External':
            target = data['Target']
            data['Target'] = target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(directory, target))
        result[data['Id']] = data
    return result


def extract_text(root):
    return '\n'.join(''.join(t.text or '' for t in p.findall('.//a:t', NS))
                     for p in root.findall('.//a:p', NS))


def extract_deck(path, label):
    rows = []
    with zipfile.ZipFile(path) as archive:
        pres = ET.fromstring(archive.read('ppt/presentation.xml'))
        rels = relationships(archive, 'ppt/presentation.xml')
        # Follow presentation order, not numeric XML filenames.
        for number, slide in enumerate(pres.findall('p:sldIdLst/p:sldId', NS), 1):
            part = rels[slide.get('{' + NS['r'] + '}id')]['Target']
            root = ET.fromstring(archive.read(part))
            text = extract_text(root)
            slide_rels = relationships(archive, part)
            note_parts = []
            for rel in slide_rels.values():
                if rel['Type'].endswith('/notesSlide'):
                    note_root = ET.fromstring(archive.read(rel['Target']))
                    for shape in note_root.findall('.//p:sp', NS):
                        ph = shape.find('.//p:ph', NS)
                        if ph is not None and ph.get('type') in ['sldNum', 'hdr', 'ftr', 'dt']:
                            continue
                        note_parts.append(extract_text(shape))
            rows.append(dict(deck=label, file=path.name, slide=number,
                             title=next((s for s in text.splitlines() if s.strip()), ''),
                             text=text, notes='\n'.join(note_parts).strip(),
                             hidden=root.get('show') == '0', xml_part=part,
                             links=[r['Target'] for r in slide_rels.values()
                                    if r['Type'].endswith('/hyperlink') and r.get('TargetMode') == 'External']))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seoul', type=Path, required=True)
    parser.add_argument('--berlin', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=ROOT / 'references')
    args = parser.parse_args()
    # Complete extraction before changing any existing corpus.
    extracted = [(label, path, extract_deck(path, label))
                 for label, path in [('seoul', args.seoul), ('berlin', args.berlin)]]
    output = args.output
    (output / 'corpus').mkdir(parents=True, exist_ok=True)
    manifest_path = output / 'sources.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else []
    manifest = [s for s in manifest if s['id'] not in ['seoul', 'berlin']]
    for label, path, rows in extracted:
        (output / 'corpus' / (label + '.jsonl')).write_text(
            ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf-8')
        outline = f'# {path.name}\n\n번호는 PPTX 내부의 실제 발표 순서(1부터)입니다. 그림의 OCR은 포함하지 않습니다.\n\n| 슬라이드 | 첫 텍스트 | 노트 |\n|---:|---|---|\n'
        outline += ''.join(f"| {r['slide']} | {r['title'].replace('|', ' / ')} | {'있음' if r['notes'] else '없음'} |\n" for r in rows)
        (output / (label + '-outline.md')).write_text(outline, encoding='utf-8')
        manifest.append(dict(id=label, file=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                             slides=len(rows), slides_with_notes=sum(bool(r['notes']) for r in rows),
                             kind='local-pptx', extracted_at=datetime.datetime.now(datetime.timezone.utc).isoformat()))
        print(f"{label}: {len(rows)} slides; {sum(bool(r['notes']) for r in rows)} with notes")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
