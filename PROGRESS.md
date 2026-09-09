# PROGRESS / HANDOFF NOTES (read this first after any context compaction)

## Task (verbatim intent)
Create the most comprehensive, detailed, well-researched review/guide on mastering
solo masturbation for males and everything related to it. Deliverables:
1. A Markdown document (`GUIDE.md` — single master doc; chapters also in `docs/chapters/`)
2. A website (static, in `site/`) that presents the same content nicely.

No word/time limit. Be thorough. Framing: adult (18+) sexual-health / wellness
education — anatomy, physiology, technique, health, psychology, safety, myths,
toys, lubricants, hygiene, compulsivity awareness, etc. Written like a good sex
educator / men's-health resource: frank, non-judgmental, evidence-informed,
non-pornographic (no explicit erotica, no minors, no illegal content).

## Workflow rules (from user)
- Push straight to `main`. NO branches, NO PRs.
- Commit + push after EVERY meaningful chunk of work (workflow may be killed
  at any time due to credits).
- Context compaction will happen. This file + git log are the memory.
- Keep documenting reasoning/decisions here.

## Repo
- Remote: https://github.com/gorg667/gooning-guide.git (branch main)
- Credentials configured via setup_github_environment.

## Architecture decisions
- Content is authored as separate chapter markdown files in `docs/chapters/NN-slug.md`.
- `scripts/build.py` concatenates chapters -> `GUIDE.md` and renders each chapter
  to HTML in `site/` (static site, no framework, Python `markdown` lib; vanilla
  CSS/JS, dark/light theme, sidebar TOC, search). Zero external build deps
  beyond `pip install markdown`.
- Website is a static site → can be served via `python -m http.server` in
  `site/` for preview; deployable to GitHub Pages (`site/` folder) or any host.
- Age gate / 18+ notice on the website landing page.
- Each chapter ends with a "Key takeaways" box; references listed in a
  dedicated references chapter with real, checkable sources (studies, medical
  orgs). Cite conservatively; where evidence is weak, say so.

## Chapter plan (status: [ ] todo, [~] in progress, [x] done)
00 [x] Front matter / how to use this guide / disclaimer
01 [x] Introduction: why a guide, philosophy of "mastery", myths vs reality
02 [x] Anatomy of the male sexual system (penis, glans, frenulum, foreskin,
       corona, scrotum/testes, perineum, prostate, pelvic floor, nerves)
03 [x] Physiology of arousal, erection, ejaculation & orgasm (sexual response
       cycle, neurochemistry, refractory period, ejaculation vs orgasm)
04 [x] Health effects: what the science actually says (benefits, non-effects,
       risks, prostate research, testosterone myths, frequency)
05 [x] Hygiene, skin care & injury prevention (friction, chafing, death grip,
       foreskin care, penile fracture, Peyronie's awareness)
06 [x] Fundamentals of technique (grips, strokes, pressure, speed, hand
       positions, dry vs lubricated, circumcised vs uncircumcised differences)
07 [x] Lubricants: deep dive (water/silicone/oil/hybrid, ingredients to avoid,
       compatibility with toys/condoms, DIY cautions)
08 [x] Setting, mindset & mindfulness (environment, privacy, breathing,
       body-awareness, sensate focus applied to solo)
09 [x] Edging, stamina & arousal control (arousal scale, stop-start, squeeze,
       PC muscle role, implications for PE)
10 [x] Pelvic floor / Kegels / reverse Kegels for men (evidence, routine,
       overtraining, hypertonic pelvic floor)
10b[x] PLEASURE MAXIMIZATION (user explicitly requested): the science of
       pleasure (dopamine/anticipation vs opioid/consummation), the arousal
       "stack" model, novelty & habituation, sensory layering (touch, temp,
       sound, scent, visual), anticipation/denial/teasing, varying speed &
       pressure, whole-body erogenous mapping, timing (circadian, post-
       exercise, after abstinence), breath & sound, orgasm intensity
       factors (build-up duration, pelvic floor state, edging count,
       prostate involvement, abstinence duration), "orgasm quality
       journaling", sessions design (short/medium/long), afterglow.
11 [x] Advanced sensations: non-ejaculatory & multiple orgasms, prostate
       stimulation (external & internal), perineum, nipples, full-body
       arousal, breathwork approaches — evidence-rated
12 [x] Toys & devices (sleeves/strokers, rings, prostate massagers, vibrators,
       automated devices, materials safety, cleaning, storage, buying guide)
13 [x] Fantasy, erotica & pornography: healthy use, habituation/tolerance,
       "porn-induced ED" debate, the evidence both ways, practical guidelines
14 [x] Compulsivity, "gooning", frequency & when it's a problem (CSBD ICD-11,
       self-assessment, moderation strategies, seeking help)
15 [x] Common problems & troubleshooting (delayed ejaculation, death grip
       syndrome, PE, ED, loss of sensitivity, pain, blood in semen, post-
       orgasmic illness syndrome, retrograde ejaculation)
16 [x] Masturbation across life stages & circumstances (adolescence-adult,
       aging, relationships, long-distance, after illness/surgery, disability)
17 [x] Diet, sleep, exercise, substances & sexual function (what matters,
       what doesn't, supplements skepticism)
18 [x] Culture, religion, history & stigma (brief scholarly overview)
19 [x] Ethics, privacy & digital safety (consent-related content ethics,
       device/data hygiene, cam/sexting risks, legal notes)
20 [x] Practice programs: 4-week beginner, 8-week intermediate, ongoing
       advanced routines; journaling templates
21 [x] FAQ (100+ questions)
22 [x] Glossary
23 [x] References & further reading (books, studies, orgs, hotlines)

## Build/site status
- [ ] scripts/build.py
- [ ] site/ CSS/JS template
- [ ] README.md

## Log (append newest at bottom)
- 2026-09-09: Repo empty. Created PROGRESS.md, planned architecture & chapters.

- Ch00-10 written & pushed. Ch10 was lost once to interruption and rewritten. NEXT: ch11 pleasure-maximization (user-emphasized), then 12..23, then build script + site.
- Ch19 lost to interruption once, rewritten. Remaining: 20 ethics/privacy, 21 programs, 22 FAQ, 23 glossary, 24 references, then build.py + site.
- ALL 25 chapter files (00-24) done. NEXT: scripts/build.py -> GUIDE.md + site/, README.md, then preview & verify.
