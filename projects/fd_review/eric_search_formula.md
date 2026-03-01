# ERIC Search Formula

PubMed検索式をERIC形式に変換した結果

## #1 Target Audience (対象者)

### Original PubMed:
```
"Faculty, Medical"[Mesh] OR medical faculty[tiab] OR clinical educator*[tiab] OR clinician educator*[tiab] OR medical educator*[tiab] OR clinical teacher*[tiab] OR clinical teaching[tiab]
```

### ERIC Conversion:
```
(subject:"Medical School Faculty" OR subject:"College Faculty" OR title:"medical faculty" OR title:"clinical educator" OR title:"clinician educator" OR title:"medical educator" OR title:"clinical teacher" OR title:"clinical teaching")
```

#1 Hits: 65,264 hits

---

## #2 Intervention (介入)

### Original PubMed:
```
"Staff Development"[Mesh] OR "Program Development"[Mesh] OR faculty development*[tiab] OR professional development*[tiab] OR teaching skill*[tiab] OR "program design"[tiab]
```

### ERIC Conversion:
```
(subject:"Faculty Development" OR subject:"Professional Development" OR subject:"Staff Development" OR subject:"Program Development" OR subject:"Program Design" OR title:"faculty development" OR title:"professional development" OR title:"teaching skill" OR title:"program design")
```

#2 Hits: 122,708 hits

---

## #3 Combined (#1 AND #2)

### ERIC Formula:
```
(subject:"Medical School Faculty" OR subject:"College Faculty" OR title:"medical faculty" OR title:"clinical educator" OR title:"clinician educator" OR title:"medical educator" OR title:"clinical teacher" OR title:"clinical teaching") AND (subject:"Faculty Development" OR subject:"Professional Development" OR subject:"Staff Development" OR subject:"Program Development" OR subject:"Program Design" OR title:"faculty development" OR title:"professional development" OR title:"teaching skill" OR title:"program design")
```

#3 Hits: 8,740 hits

---

## Summary

| Block | Description | Hits |
|-------|-------------|------|
| #1 | Target Audience | 65,264 |
| #2 | Intervention | 122,708 |
| #3 | Combined | 8,740 |

## Sample Results (Top 5)

### [1] ED576485
- **Title**: A Professional Development Program for Dental Medical Educators in Kuwait: Needs Assessment, Program Design and Formative Evaluation
- **Year**: 2017
- **Source**: N/A
- **Descriptors**: Foreign Countries, Medical School Faculty, Dental Schools, Faculty Development, Needs Assessment, Case Method (Teaching Technique), Problem Based Learning, Mixed Methods Research

### [2] EJ363738
- **Title**: An Adaptive Faculty Development Program for Improving Teaching Skills.
- **Year**: 1987
- **Source**: N/A
- **Descriptors**: Dental Schools, Experimental Programs, Faculty Development, Higher Education, Instructional Improvement, Lecture Method, Medical School Faculty, Professional Education

### [3] EJ609920
- **Title**: A Theory-based Faculty Development Program for Clinician-Educators.
- **Year**: 2000
- **Source**: N/A
- **Descriptors**: College Faculty, Faculty Development, Higher Education, Instructional Improvement, Medical Education, Program Evaluation

### [4] EJ455975
- **Title**: Professional Development: An Integrated Strategy at the University of New South Wales.
- **Year**: 1992
- **Source**: N/A
- **Descriptors**: Administrator Education, College Administration, College Faculty, Departments, Faculty Development, Foreign Countries, Higher Education, Professional Development

### [5] EJ127981
- **Title**: How Do We Get There From Here? Program Design for Faculty Development
- **Year**: 1975
- **Source**: N/A
- **Descriptors**: Administrator Attitudes, College Faculty, Higher Education, Institutional Environment, Instructional Improvement, Models, Professional Continuing Education, Program Design

---

## Conversion Notes

### PubMed → ERIC Mapping

| PubMed | ERIC | Notes |
|--------|------|-------|
| `[Mesh]` | `subject:"Term"` | ERICのDescriptor (シソーラス) |
| `[tiab]` | `title:"phrase"` | ERICはtitle+abstractの複合フィールドなし |
| `term*` | `term*` | ワイルドカードは同じ |

### ERIC Thesaurus Mapping

| PubMed MeSH | ERIC Descriptor |
|-------------|-----------------|
| Faculty, Medical | Medical School Faculty |
| Staff Development | Staff Development, Faculty Development |
| Program Development | Program Development, Program Design |
