# physician-pt Report: #4 (Physiotherapy/Rehabilitation) Block Impact

## Purpose
Summarize the effect of adding the #4 physiotherapy/rehabilitation block to the current PubMed query, so co-authors can decide whether to keep or drop it.

## Query Versions Compared

### A) Without #4
```
#1 ("Interprofessional Relations"[Mesh] OR "Interdisciplinary Communication"[Mesh] OR interprofessional*[tiab] OR inter-professional*[tiab] OR interdisciplinary*[tiab] OR inter-disciplinary*[tiab] OR multidisciplinary*[tiab] OR multi-disciplinary*[tiab] OR team[tiab])
#2 (barrier*[tiab] OR obstacle*[tiab] OR challenge*[tiab] OR hinder*[tiab] OR constraint*[tiab] OR facilitator*[tiab] OR enabler*[tiab] OR bridging*[tiab])
#3 ("Systematic Review"[Publication Type] OR  review[pt] OR "systematic review"[pt] OR "meta-analysis"[pt] OR "scoping review"[tiab] OR "scoping reviews"[tiab] OR "systematic review"[tiab] OR "systematic reviews"[tiab] OR "umbrella review"[tiab] OR "umbrella reviews"[tiab])
#4 #1 AND #2 AND #3
```
Result count: **21,246**

Seed capture: **5/5**
- 37860510: captured
- 35065048: captured
- 39920051: captured
- 31329469: captured
- 36475911: captured

Source log: `projects/physician-pt/log/search_lines_20250214_v9.md`

### B) With #4 (Physiotherapy/Rehabilitation Block)
```
#1 ("Interprofessional Relations"[Mesh] OR "Interdisciplinary Communication"[Mesh] OR interprofessional*[tiab] OR inter-professional*[tiab] OR interdisciplinary*[tiab] OR inter-disciplinary*[tiab] OR multidisciplinary*[tiab] OR multi-disciplinary*[tiab] OR team[tiab])
#2 (barrier*[tiab] OR obstacle*[tiab] OR challenge*[tiab] OR hinder*[tiab] OR constraint*[tiab] OR facilitator*[tiab] OR enabler*[tiab] OR bridging*[tiab])
#3 ("Systematic Review"[Publication Type] OR  review[pt] OR "systematic review"[pt] OR "meta-analysis"[pt] OR "scoping review"[tiab] OR "scoping reviews"[tiab] OR "systematic review"[tiab] OR "systematic reviews"[tiab] OR "umbrella review"[tiab] OR "umbrella reviews"[tiab])
#4 ("Physical Therapists"[Mesh] OR "Physical Therapy Modalities"[Mesh] OR physiotherap*[tiab] OR "physical therap*"[tiab] OR "physical therapist*"[tiab] OR rehabilitation*[tiab])
#5 #1 AND #2 AND #3 AND #4
```
Result count: **1,163**

Seed capture: **4/5**
- 37860510: captured
- 35065048: captured
- 39920051: captured
- 31329469: **not captured**
- 36475911: captured

Source log: `projects/physician-pt/log/search_lines_20250214_v11.md`

### C) With #4 (Physiotherapy Only, Excluding rehabilitation*)
```
#1 ("Interprofessional Relations"[Mesh] OR "Interdisciplinary Communication"[Mesh] OR interprofessional*[tiab] OR inter-professional*[tiab] OR interdisciplinary*[tiab] OR inter-disciplinary*[tiab] OR multidisciplinary*[tiab] OR multi-disciplinary*[tiab] OR team[tiab])
#2 (barrier*[tiab] OR obstacle*[tiab] OR challenge*[tiab] OR hinder*[tiab] OR constraint*[tiab] OR facilitator*[tiab] OR enabler*[tiab] OR bridging*[tiab])
#3 ("Systematic Review"[Publication Type] OR  review[pt] OR "systematic review"[pt] OR "meta-analysis"[pt] OR "scoping review"[tiab] OR "scoping reviews"[tiab] OR "systematic review"[tiab] OR "systematic reviews"[tiab] OR "umbrella review"[tiab] OR "umbrella reviews"[tiab])
#4 ("Physical Therapists"[Mesh] OR "Physical Therapy Modalities"[Mesh] OR physiotherap*[tiab] OR "physical therap*"[tiab] OR "physical therapist*"[tiab])
#5 #1 AND #2 AND #3 AND #4
```
Result count: **406**

Seed capture: **3/5**
- 37860510: captured
- 35065048: **not captured**
- 39920051: captured
- 31329469: **not captured**
- 36475911: captured

Source log: `projects/physician-pt/log/search_lines_20250214_v10.md`

## Notes for Discussion
- Adding #4 reduces results from **21,246 → 1,163**.
- The seed lost with #4 is **PMID 31329469** (interprofessional collaboration review without explicit rehabilitation/physiotherapy wording).
