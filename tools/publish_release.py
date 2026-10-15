"""Publish the locally tested package without rebuilding it on the runner."""
import hashlib
import json
import os
import pathlib
import urllib.error
import urllib.parse
import urllib.request

root = pathlib.Path(__file__).resolve().parent.parent
repo = os.environ['GITHUB_REPOSITORY']
token = os.environ['GITHUB_TOKEN']
tag = 'v1.0.2'
api = 'https://api.github.com/repos/' + repo
headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}

def request(url, method='GET', data=None, content_type='application/json'):
    request_headers = dict(headers)
    if data is not None:
        request_headers['Content-Type'] = content_type
    req = urllib.request.Request(url, data=data, headers=request_headers, method=method)
    with urllib.request.urlopen(req, timeout=120) as response:
        return json.load(response)

checksums = {}
for line in (root / 'downloads/SHA256SUMS.txt').read_text().splitlines():
    digest, name = line.split('  ', 1)
    path = root / 'downloads' / name
    if path.parent != root / 'downloads':
        raise ValueError('Invalid artifact name')
    if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise ValueError('Artifact checksum mismatch: ' + name)
    checksums[name] = digest

try:
    release = request(api + '/releases/tags/' + tag)
except urllib.error.HTTPError as error:
    if error.code != 404:
        raise
    release = request(api + '/releases', 'POST', json.dumps({
        'tag_name': tag, 'target_commitish': os.environ['GITHUB_SHA'],
        'name': 'v1.0.2 · QQ 音乐原生播放器一键部署包',
        'body': (root / 'RELEASE_TEXT.md').read_text(encoding='utf-8-sig'),
        'draft': False, 'prerelease': False,
    }).encode())

existing = {asset['name']: asset for asset in release['assets']}
for name in list(checksums) + ['SHA256SUMS.txt']:
    path = root / 'downloads' / name
    data = path.read_bytes()
    digest = 'sha256:' + hashlib.sha256(data).hexdigest()
    if name in existing:
        if existing[name].get('digest') != digest:
            raise ValueError('Existing release asset differs; refusing to overwrite: ' + name)
        print('Already verified:', name)
        continue
    upload = release['upload_url'].split('{', 1)[0] + '?' + urllib.parse.urlencode({'name': name})
    asset = request(upload, 'POST', data, 'application/octet-stream')
    if asset['size'] != len(data) or (asset.get('digest') and asset['digest'] != digest):
        raise ValueError('Uploaded artifact verification failed')
    print('Published:', asset['browser_download_url'])
print('Release:', release['html_url'])
