#!/usr/bin/env python3

from scripts.conversion.ovid.converter import convert_ovid_to_pubmed

def main():
    ovid_query = """(exp Helicobacter/ or exp Helicobacter Infections/ or (helicobacter or campylobacter).tw,kw. or (pylori or pyloridis or HP).tw,kw.) and (exp Anti-Inflammatory Agents, Non-Steroidal/ or nsaid*.tw,kw. or non steroid* anti?inflammator*.tw,kw. or non steroid* anti inflammator*.tw,kw. or non?steroid* anti inflammator*.tw,kw. or non?steroid* anti?inflammator*.tw,kw.) and (((exp stomach/ or stomach.tw,kw. or gastr*.tw,kw. or exp duodenum/ or duoden*.tw,kw.) and (peptic*.tw,kw. or exp peptic ulcer/)) or (peptic adj5 ulcer*).tw,kw. or (stomach adj5 ulcer*).tw,kw. or (duoden* adj5 ulcer*).tw,kw. or (gastroduoden* adj5 ulcer*).tw,kw.)"""
    
    print("Original Ovid MEDLINE Query:")
    print(ovid_query)
    print("\n" + "="*80 + "\n")
    
    pubmed_query, warnings = convert_ovid_to_pubmed(ovid_query)
    
    print("Converted PubMed Query:")
    print(pubmed_query)
    
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")
    
    return pubmed_query

if __name__ == "__main__":
    main()
