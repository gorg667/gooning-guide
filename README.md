# The Complete Guide to Male Solo Sexuality

**An evidence-informed handbook on masturbation mastery, pleasure, health, and self-knowledge.**
Adults (18+) only. Educational, not pornographic. Not medical advice.

- 24 chapters · ~61,000 words
- Anatomy, physiology, the science of health effects, hygiene and injury prevention, technique fundamentals, lubricants, mindset and mindfulness, edging and arousal control, pelvic floor training, **pleasure maximization**, prostate and non-ejaculatory/multiple orgasms, toys and materials safety, fantasy/erotica/pornography evidence review, compulsivity and "gooning," troubleshooting every common problem, life stages, lifestyle and substances, cultural history, privacy and digital safety, structured 4-week / 8-week / ongoing practice programs, FAQ, glossary, and a full reference list.
- Every health claim is evidence-rated: 🟢 strong · 🟡 moderate · 🟠 weak/anecdotal · 🔴 contradicted.

## Deliverables

| What | Where |
|---|---|
| **Single Markdown document** | [`GUIDE.md`](GUIDE.md) (generated; also at `site/GUIDE.md`) |
| **Website** (static, no framework) | [`site/`](site/) — open `site/index.html` |
| Chapter sources | [`docs/chapters/`](docs/chapters/) |
| Build script | [`scripts/build.py`](scripts/build.py) |
| Research notes & sources | [`docs/RESEARCH_NOTES.md`](docs/RESEARCH_NOTES.md), Chapter 24 |

## Build

```bash
pip install markdown pymdown-extensions
python3 scripts/build.py          # -> GUIDE.md and site/
python3 -m http.server -d site 8080   # preview at http://localhost:8080
```

`build.py` concatenates `docs/chapters/*.md` into `GUIDE.md`, renders each chapter to HTML with a sidebar, per-page TOC, client-side search (`search.json`), dark/light theme, and an 18+ age gate.

## Deploy to GitHub Pages

The `site/` folder is committed, so the simplest path is:

1. Repo **Settings → Pages → Build and deployment → Source: Deploy from a branch**
2. Branch `main`, folder `/site` → Save.

Alternatively, copy `docs/deploy/github-pages-workflow.yml` to `.github/workflows/pages.yml` (it rebuilds on every push and deploys via Actions). It lives in `docs/deploy/` because the automation token used to write this repo lacks the `workflows` scope.

## Editing

Edit or add files in `docs/chapters/` (numbered `NN-slug.md`, each starting with a single `# Title`), then re-run the build. Chapters should end with a `### Key takeaways` section — the site styles it as a callout box.

## Structure of the guide

```
00 Front matter · how to use · disclaimer
01 Introduction: why mastery; myths table
02 Anatomy                      13 Toys, sleeves & devices
03 Physiology                   14 Fantasy, erotica & pornography
04 Health: what science says    15 Frequency, compulsivity & "gooning"
05 Hygiene, skin & injury       16 Troubleshooting (PE, DE, ED, pain, POIS…)
06 Technique fundamentals       17 Life stages & circumstances
07 Lubricants                   18 Body, lifestyle, substances, supplements
08 Setting, mindset, mindfulness 19 Culture, religion, history, stigma
09 Edging & arousal control     20 Ethics, privacy & digital safety
10 Pelvic floor                 21 Practice programs & journaling
11 Pleasure maximization        22 FAQ · 23 Glossary · 24 References
12 Advanced sensations
```

## License

Content © the repository owner. Cite sources per Chapter 24 when reusing factual claims.
