#!/usr/bin/env python3
"""
Check combined query hit count: P-Block (corrected) AND Concept Block (Narrative).
"""

import time
import requests
from typing import Dict

ENTREZ_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

def count_pubmed_hits(term: str, label: str = "") -> int:
    """Query PubMed and return hit count."""
    try:
        params = {
            "db": "pubmed",
            "term": term,
            "retmax": 0,
            "retmode": "json"
        }
        response = requests.get(ENTREZ_BASE_URL, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        count = int(data["esearchresult"]["count"])
        if label:
            print(f"{label}: {count:,} hits")
        return count
    except Exception as e:
        print(f"Error querying: {e}")
        return -1

def main():
    print("# Combined Query Analysis: P-Block (Corrected) AND Concept Block\n")

    # P-Block (修正後 - seach_formula_2.md)
    p_block = (
        '"Medically Unexplained Symptoms"[Mesh] OR "Somatoform Disorders"[Mesh] OR '
        '"Psychophysiologic Disorders"[Mesh] OR "chronic pain"[Mesh] OR '
        '"Central Nervous System Sensitization"[Mesh] OR "Nociplastic Pain"[Mesh] OR '
        '"Polydipsia, Psychogenic"[Mesh] OR "Psychogenic Nonepileptic Seizures"[Mesh] OR '
        '"Hearing Loss, Functional"[Mesh] OR "psychogenic syncope"[Supplementary Concept] OR '
        '"Orthostatic Intolerance"[Mesh] OR "somatic cough syndrome"[Supplementary Concept] OR '
        '"Fibromyalgia"[Mesh] OR "Fatigue Syndrome, Chronic"[Mesh] OR '
        '"Colonic Diseases, Functional"[Mesh] OR '
        '"Temporomandibular Joint Dysfunction Syndrome"[Mesh] OR '
        '"Cystitis, Interstitial"[Mesh] OR "Multiple Chemical Sensitivity"[Mesh] OR '
        '"persistent somatic symptom*"[tiab] OR "persistent physical symptom*"[tiab] OR '
        '"medically unexplained symptom*"[tiab] OR '
        '"Medically Unexplained Physical Symptom*"[tiab] OR '
        '"functional somatic disorder*"[tiab] OR "Somatic symptom disorder*"[tiab] OR '
        '"functional somatic syndrome*"[tiab] OR "somatisation"[tiab] OR '
        '"somatization"[tiab] OR "bodily distress syndrome*"[tiab] OR '
        '"chronic pain"[tiab] OR "Chronic primary pain"[tiab] OR '
        '"Chronic widespread pain"[tiab] OR "Functional Pain"[tiab] OR '
        '"Central Nervous System Sensitization"[tiab] OR "Nociplastic Pain"[tiab] OR '
        '"Psychogenic Polydipsia"[tiab] OR "Psychogenic Nonepileptic Seizure*"[tiab] OR '
        '"Functional Hearing Loss"[tiab] OR "psychogenic syncope"[tiab] OR '
        '"Orthostatic Intolerance"[tiab] OR '
        '"Postural Orthostatic Tachycardia Syndrome"[tiab] OR '
        '"somatic cough syndrome*"[tiab] OR "Fibromyalgia"[tiab] OR '
        '"Chronic Fatigue Syndrome*"[tiab] OR "Chronic fatigue"[tiab] OR '
        '"Irritable bowel syndrome"[tiab] OR "Functional Neurological Disorder*"[tiab] OR '
        '"Temporomandibular Joint Dysfunction Syndrome"[tiab] OR '
        '"interstitial cystitis"[tiab] OR "dyspareunia"[tiab] OR '
        '"Multiple Chemical Sensitivity"[tiab] OR '
        '"Disorders of gut brain interaction"[tiab] OR "Myalgic Encephalopathy"[tiab] OR '
        '"Myalgic Encephalomyelitis"[tiab] OR "Non-organic"[tiab] OR '
        '"Persistent symptoms"[tiab:~2] OR "Functional symptoms"[tiab:~2] OR '
        '"Functional syndrome"[tiab:~2] OR "Functional gut"[tiab:~2]'
    )

    # Concept Block (Narrative Approach from search_formula_initial.md)
    concept_block = (
        '"Narrative Medicine"[Mesh] OR "Narration"[Mesh] OR '
        '"Patient-Centered Care"[Mesh] OR "narrative approach*"[tiab] OR '
        '"narrative medicine"[tiab] OR "narrative based medicine"[tiab] OR '
        '"illness narrative*"[tiab] OR "storytelling"[tiab] OR '
        '"meaning making"[tiab] OR "Patient-Centered Care"[tiab] OR '
        '"re-authoring"[tiab] OR "sage consultation"[tiab] OR '
        '"expert generalist"[tiab] OR "narrative construction"[tiab] OR '
        '"illness experience*"[tiab]'
    )

    # Primary Care Block (Context)
    context_block = (
        '"Primary Health Care"[Mesh] OR "General Practice"[Mesh] OR '
        '"Physicians, Family"[Mesh] OR "primary care"[tiab] OR '
        '"general practice"[tiab] OR "family practice"[tiab] OR '
        '"family medicine"[tiab] OR "general practitioner*"[tiab]'
    )

    print("## Individual Block Counts\n")

    p_count = count_pubmed_hits(p_block, "**P-Block (Corrected PPS)**")
    time.sleep(0.34)

    concept_count = count_pubmed_hits(concept_block, "**Concept Block (Narrative)**")
    time.sleep(0.34)

    context_count = count_pubmed_hits(context_block, "**Context Block (Primary Care)**")
    time.sleep(0.34)

    print("\n## Combined Query Counts\n")

    # P AND Concept
    p_and_concept = f"({p_block}) AND ({concept_block})"
    p_concept_count = count_pubmed_hits(p_and_concept, "**P AND Concept**")
    time.sleep(0.34)

    # P AND Concept AND Context
    p_and_concept_and_context = f"({p_block}) AND ({concept_block}) AND ({context_block})"
    final_count = count_pubmed_hits(p_and_concept_and_context, "**P AND Concept AND Context (Final)**")

    print("\n## Summary\n")
    print(f"| Query | Hit Count |")
    print(f"|---|---|")
    print(f"| P-Block (PPS) | {p_count:,} |")
    print(f"| Concept Block (Narrative) | {concept_count:,} |")
    print(f"| Context Block (Primary Care) | {context_count:,} |")
    print(f"| **P AND Concept** | **{p_concept_count:,}** |")
    print(f"| **P AND Concept AND Context** | **{final_count:,}** |")

    if p_count > 0 and concept_count > 0:
        overlap_rate = (p_concept_count / min(p_count, concept_count)) * 100
        print(f"\nOverlap rate (P ∩ Concept / smaller block): {overlap_rate:.2f}%")

if __name__ == "__main__":
    main()
