"""Lấy số liệu tác động của từng dự án và ghi vào data/metrics.json.

Chạy: python3 metrics.py   (GitHub Actions chạy hằng tuần, xem .github/workflows/rank.yml)
Nguồn: OpenAlex (trích dẫn theo DOI), Zenodo (lượt tải, lượt xem), GitHub (số sao).
Nguồn nào lỗi mạng thì giữ nguyên số cũ của nguồn đó.
"""
import json, os, urllib.request, urllib.parse, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'data', 'metrics.json')
UA = {'User-Agent': 'zhaninh.github.io-metrics'}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
        return json.load(r)


def citations(doi):
    return get('https://api.openalex.org/works/doi:' + urllib.parse.quote(doi, safe='/:.') + '?select=cited_by_count')['cited_by_count']


def zenodo(rec):
    s = get(f'https://zenodo.org/api/records/{rec}')['stats']
    return s.get('unique_downloads', 0), s.get('unique_views', 0)


def stars(repo):
    return get(f'https://api.github.com/repos/{repo}')['stargazers_count']


def main():
    import build  # dùng chung danh sách WORK
    old = json.load(open(OUT)) if os.path.exists(OUT) else {}
    new = {}
    for w in build.WORK:
        im = w.get('impact', {}); m = dict(old.get(w['slug'], {}))
        try:
            m['citations'] = sum(citations(d) for d in im.get('dois', []))
        except Exception as e:
            print('openalex', w['slug'], e)
        try:
            dl = vw = 0
            for rec in im.get('zenodo', []):
                a, b = zenodo(rec); dl += a; vw += b
            m['downloads'], m['views'] = dl, vw
        except Exception as e:
            print('zenodo', w['slug'], e)
        try:
            m['stars'] = sum(stars(r) for r in im.get('github', []))
        except Exception as e:
            print('github', w['slug'], e)
        new[w['slug']] = m
    new['_updated'] = datetime.date.today().isoformat()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(new, open(OUT, 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(new, indent=1))


if __name__ == '__main__':
    main()
