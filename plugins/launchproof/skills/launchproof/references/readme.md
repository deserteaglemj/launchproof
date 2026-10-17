# README guide

The README is the landing page, the install doc and the source most AI answers quote. Write it for three readers at once: a person deciding in 10 seconds, a person installing, and an agent answering "what tool does X?".

## Order

1. **Hero.** Name, a hero image or H1, 3 to 5 badges (license, CI from `actions/workflows/<file>/badge.svg`, release, eval result if real), then one bold sentence that says what it is, who it is for and the key difference: "**name is a <category> for <who>: it <does X> <how>.**" Use the words people search for (the category name, the input and output) in that first sentence.
2. **Demo.** A GIF, short video or screenshot within the first screen. Make it from the real tool on your own sample content. Never a third-party logo or a real company's site.
3. **Quickstart.** The shortest path to a first result: install, one command, what you should see. Copy-pasteable code blocks, one command per block.
4. **What a run looks like / How it works.** A short numbered list or diagram.
5. **Proof.** Real numbers from evals, tests or benchmarks, with the command that produced them and a link to the results file in the repo (`evals/RESULTS.md`). The audit checks that numbers in this section appear in the linked file. If there are no numbers yet, run the project's tests or evals now and publish those; never invent or round up.
6. **How it compares.** A table or short list against 2 to 4 real alternatives. Rules: link each alternative's own page as the source, say where the alternative is stronger, compare like with like, date the comparison ("as of 2026-10"), and avoid "better" without a measured reason.
7. **Limitations.** At least 3 honest bullets: what it does not do, where it is weak, what it needs installed, how small the eval set is.
8. **FAQ.** 6 to 10 questions written the way people ask an AI assistant or a search box, each answered in 1 to 3 sentences that stand alone (an agent may quote one answer without the rest). Format: `**How do I <task> with <tool>?** Answer.` Cover: how to do the core task, "is there a X that needs no Y", "how is this different from <named alternative>", "does it work with <host/platform>", "does it send my data anywhere", "what does it cost / need".
9. **Contributing, Security, License, Credits.** One line each, linking the files. Credit prior art and anything reused.

## Claims

- Every number links to its evidence in the repo.
- No "first", "only", "best", "fastest", "leading", "revolutionary", "state of the art", "#1". Say what it does and what was measured.
- Version numbers in README, manifests and CHANGELOG match.
- Do not name private clients, employers or companies you worked for unless they approved it in writing.

## Style

- Short sentences, plain words, active voice. Headings are nouns or questions.
- Code blocks are runnable as written. Use `~` or relative paths, never a personal absolute path.
- Images have alt text. Relative links resolve (the audit checks this).

Credits: section order draws on ideas from othneildrew/Best-README-Template (Unlicense) and matiassingers/awesome-readme (ideas only, linked not copied).
