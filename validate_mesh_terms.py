import sys
sys.path.append('scripts/search/mesh_analyzer')
from check_mesh import check_mesh_term
import time

mesh_terms = [
    'Social Isolation',
    'quarantine',
    'Computers, Handheld',
    'Internet',
    'Telecommunications',
    'Telemedicine',
    'Cell Phone',
    'Remote Sensing Technology',
    'Wearable Electronic Devices'
]

print('MeSH用語の確認を開始します...\n')

for term in mesh_terms:
    time.sleep(1)
    result = check_mesh_term(term)
    print(f'用語: {result["term"]}')
    print(f'存在: {"はい" if result["exists"] else "いいえ"}')
    print(f'MeSHデータベースでの出現数: {result["mesh_count"]}')
    print(f'PubMedでの文献数: {result["pubmed_count"]}')
    if result["message"] != 'Success':
        print(f'メッセージ: {result["message"]}')
    print('-' * 50)
