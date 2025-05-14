# データベース別検索式

変換日時: 2025-05-14 08:24:28

## PubMed

```
#1 "Essential Tremor"[Mesh]
#2 "tremor therapy"[tiab:~2]
#3 "deep brain"[Title:~0]
#4 "hospital university"[ad:~5]
#5 (#1 OR #2) AND (#3 OR #4)

```

## Cochrane CENTRAL

```
#1 [mh "Essential Tremor"]
#2 ("tremor" NEAR/2 "therapy"):ti,ab,kw
#3 ("deep" NEXT "brain"):ti
#4 ("hospital" NEAR/5 "university")
#5 (#1 OR #2) AND (#3 OR #4)
```

## Dialog (Embase)

```
S1 EMB.EXACT.EXPLODE("Essential Tremor")
S2 TI,AB(tremor N/2 therapy)
S3 TI(deep W/1 brain)
S4 CS(hospital N/5 university)
S5 (S1 OR S2) AND (S3 OR S4)
```

## Command Line for Dialog

Dialog検索画面でコピー&ペーストして使用するコマンドライン形式：

```
EMB.EXACT.EXPLODE("Essential Tremor")
TI,AB(tremor N/2 therapy)
TI(deep W/1 brain)
CS(hospital N/5 university)
(S1 OR S2) AND (S3 OR S4)
```
