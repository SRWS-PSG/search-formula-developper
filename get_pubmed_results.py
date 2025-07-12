import requests
import time
import json
from xml.etree import ElementTree as ET

def get_detailed_pubmed_results():
    """Get detailed PubMed results for the final extended intervention search formula"""
    
    search_query = '((Social Isolation[mh]) OR (Loneliness[mh]) OR (loneliness[tiab]) OR ("social isolation"[tiab]) OR ("social isolat*"[tiab])) AND ((Smartphone[mh]) OR (Wearable Electronic Devices[mh]) OR (Mobile Applications[mh]) OR (smartphone*[tiab]) OR ("mobile app*"[tiab]) OR ("mobile application*"[tiab]) OR ("wearable device*"[tiab]) OR ("digital phenotyping"[tiab]) OR ("passive sensing"[tiab]) OR ("mobile health"[tiab]) OR (mhealth[tiab]) OR (Cell Phone[mh]) OR (Remote Sensing Technology[mh]) OR ("Digital Biomarkers"[tiab]) OR ("sensor data"[tiab]) OR (accelerometer[tiab]) OR ("activity monitor*"[tiab]) OR (app[tiab]) OR (apps[tiab]) OR (("cell"[tiab] or "cellular"[tiab] or "mobile"[tiab] or "smart"[tiab]) AND ("phone"[tiab] or "telephone"[tiab] or "device"[tiab] or "application"[tiab])) OR ("Handheld Computer*"[tiab]) OR ("real time data"[tiab]) OR ("Short Messag* Service*"[tiab]) OR (SMS[tiab]) OR ("text messag*"[tiab]))'
    
    target_pmids = ['31342903', '35161852', '38900745']
    out_of_scope_pmid = '36519748'
    
    print("=== PubMed検索結果取得 - 拡張Intervention Block検索式 ===")
    print(f"検索式: {search_query}")
    print()
    
    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    esearch_params = {
        'db': 'pubmed',
        'term': search_query,
        'retmode': 'json',
        'retmax': 1000,  # Get up to 1000 results for detailed analysis
        'sort': 'relevance'
    }
    
    try:
        print("📡 PubMed検索を実行中...")
        response = requests.get(esearch_url, params=esearch_params)
        response.raise_for_status()
        search_data = response.json()
        
        total_count = int(search_data['esearchresult'].get('count', 0))
        id_list = search_data['esearchresult'].get('idlist', [])
        
        print(f"✅ 検索完了: 総件数 {total_count}件")
        print(f"📋 取得件数: {len(id_list)}件（詳細分析用）")
        print()
        
        print("🎯 対象PMID包含確認:")
        captured_pmids = []
        missing_pmids = []
        
        for pmid in target_pmids:
            if pmid in id_list:
                captured_pmids.append(pmid)
                print(f"✅ PMID {pmid}: 包含確認")
            else:
                missing_pmids.append(pmid)
                print(f"❌ PMID {pmid}: 未包含")
        
        if out_of_scope_pmid in id_list:
            print(f"⚠️  PMID {out_of_scope_pmid}: 包含（スコープ外のため注意）")
        else:
            print(f"✅ PMID {out_of_scope_pmid}: 未包含（スコープ外のため正しい）")
        
        print()
        print(f"📊 PMID包含サマリー: {len(captured_pmids)}/3 = {len(captured_pmids)/3*100:.1f}%")
        print()
        
        if id_list:
            print("📚 検索結果詳細（上位50件）:")
            print("-" * 80)
            
            batch_size = 50
            first_batch = id_list[:batch_size]
            
            efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            efetch_params = {
                'db': 'pubmed',
                'id': ','.join(first_batch),
                'retmode': 'xml'
            }
            
            print(f"📖 詳細情報を取得中（{len(first_batch)}件）...")
            time.sleep(1)  # Be respectful to NCBI servers
            
            detail_response = requests.get(efetch_url, params=efetch_params)
            detail_response.raise_for_status()
            
            root = ET.fromstring(detail_response.content)
            
            results_list = []
            for i, article in enumerate(root.findall('.//PubmedArticle'), 1):
                try:
                    pmid_elem = article.find('.//PMID')
                    pmid = pmid_elem.text if pmid_elem is not None else 'N/A'
                    
                    title_elem = article.find('.//ArticleTitle')
                    title = title_elem.text if title_elem is not None else 'No title available'
                    
                    authors = []
                    for author in article.findall('.//Author'):
                        lastname = author.find('LastName')
                        forename = author.find('ForeName')
                        if lastname is not None and forename is not None:
                            authors.append(f"{lastname.text} {forename.text}")
                        elif lastname is not None:
                            authors.append(lastname.text)
                    
                    author_str = ', '.join(authors[:3])  # First 3 authors
                    if len(authors) > 3:
                        author_str += ' et al.'
                    
                    year_elem = article.find('.//PubDate/Year')
                    year = year_elem.text if year_elem is not None else 'N/A'
                    
                    journal_elem = article.find('.//Journal/Title')
                    journal = journal_elem.text if journal_elem is not None else 'N/A'
                    
                    marker = ""
                    if pmid in target_pmids:
                        marker = " 🎯"
                    elif pmid == out_of_scope_pmid:
                        marker = " ⚠️"
                    
                    result_info = {
                        'rank': i,
                        'pmid': pmid,
                        'title': title,
                        'authors': author_str,
                        'year': year,
                        'journal': journal,
                        'marker': marker
                    }
                    results_list.append(result_info)
                    
                    print(f"{i:2d}. PMID: {pmid}{marker}")
                    print(f"    タイトル: {title}")
                    print(f"    著者: {author_str}")
                    print(f"    雑誌: {journal} ({year})")
                    print()
                    
                except Exception as e:
                    print(f"{i:2d}. PMID: {pmid} - 詳細取得エラー: {e}")
                    print()
            
            print("=" * 80)
            print("📈 検索結果統計:")
            print(f"総検索結果: {total_count}件")
            print(f"詳細表示: {len(results_list)}件")
            print(f"対象PMID包含: {len(captured_pmids)}/3件 ({len(captured_pmids)/3*100:.1f}%)")
            
            years = [r['year'] for r in results_list if r['year'] != 'N/A']
            if years:
                year_counts = {}
                for year in years:
                    year_counts[year] = year_counts.get(year, 0) + 1
                
                print("\n📅 発表年分布（上位50件）:")
                for year in sorted(year_counts.keys(), reverse=True)[:10]:
                    print(f"  {year}: {year_counts[year]}件")
            
            if captured_pmids:
                print(f"\n🎯 対象PMID詳細:")
                for result in results_list:
                    if result['pmid'] in captured_pmids:
                        print(f"  PMID {result['pmid']} (順位: {result['rank']})")
                        print(f"    {result['title']}")
                        print(f"    {result['authors']} - {result['journal']} ({result['year']})")
                        print()
            
            print("=" * 80)
            print("✅ PubMed検索結果取得完了")
            
            return {
                'total_count': total_count,
                'retrieved_count': len(id_list),
                'detailed_count': len(results_list),
                'captured_pmids': captured_pmids,
                'missing_pmids': missing_pmids,
                'results': results_list
            }
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None

if __name__ == "__main__":
    results = get_detailed_pubmed_results()
    if results:
        print(f"\n🎉 検索成功: {results['total_count']}件の結果を取得")
        print(f"対象PMID包含率: {len(results['captured_pmids'])}/3 = {len(results['captured_pmids'])/3*100:.1f}%")
