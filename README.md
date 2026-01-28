# Corpus Linguistics - Study 1 - Marcia

## Phase 1 - Tagging with Biber Tagger

- Tag the Bing Bang Theory TV series corpus;
- Prepare Biber's dimensions output data in Excel format.

### Lessons Learned

In most of the corpus files, contractions were not tagged correctly because they were indicated by the `’` character instead of the `'` character.

#### Original text excerpt

```
Excuse me. I’m Amy Farrah Fowler. You’re Sheldondon Cooper.
```

#### Original tagged excerpt

```
Excuse ^nn++++=Excuse
me ^pp1o+pp1+++=me.
. ^zz++++=EXTRAWORD
I ^pp1a+pp1+++=I
m ^zz++++=m
Amy ^np+++??+=Amy
Farrah ^np+++??+=Farrah
Fowler ^np+++??+=Fowler.
. ^zz++++=EXTRAWORD
You ^pp2+pp2+++=You
re ^in++++=re
Sheldondon ^np+++??+=Sheldondon
Cooper ^np++++=Cooper.
. ^zz++++=EXTRAWORD
```

#### Corrected text excerpt

```
Excuse me. I'm Amy Farrah Fowler. You're Sheldondon Cooper.
```

#### Corrected tagged excerpt

```
Excuse ^nn++++=Excuse
me ^pp1o+pp1+++=me.
. ^zz++++=EXTRAWORD
I ^pp1a+pp1+++=I'm
'm ^vb+bem+vrb++0=EXTRAWORD
Amy ^np+++??+=Amy
Farrah ^np+++??+=Farrah
Fowler ^np+++??+=Fowler.
. ^zz++++=EXTRAWORD
You ^pp2+pp2+++=You're
're ^vb+ber+vrb++0=EXTRAWORD
Sheldondon ^np+++??+=Sheldondon
Cooper ^np++++=Cooper.
. ^zz++++=EXTRAWORD
```

### Corrective action

- The issue was reproduced in the `corpus_apostrophe_test` directory;
- The original corpus and results were kept in the `corpus_original` directory;
- The `’` character was replaced by the `'` character in all the corpus files;
- The data was re-tagged with Biber Tagger.

## Phase 2 - Reprocess Tagging with Biber Tagger

- Tag the Bing Bang Theory TV series fixed corpus;
- Prepare Biber's dimensions and variables output data in Excel format.

### Lessons Learned

It was reported that a few `curly inverted commas` were not replaced by `straight quotes` in the corpus files. For instance:

```
Shame. ‘Cause I have a real zinger about my titled uterus.
```

```
Bernadette is with Priya and Leonard. Message received. Commence operation “Priya Wouldn't Wanna Be-ya.”
```

The issue was confirmed by comparing the new corpus data with the one that had been used in phase 1. Please refer to the [02_all_seasons_check_report.txt](cl_st1_ph1_marcia/corpus/02_all_seasons_check_report.txt) report for more details.
