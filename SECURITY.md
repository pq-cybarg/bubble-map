# Security & Data-Integrity Policy

This repository is **structural analysis + static web artifacts** (no server, no user data, no
secrets). "Security" here means two things: the integrity of the *claims*, and the safety of the
*static site*.

## Reporting a factual error or data problem
The strongest contribution is catching a wrong number or a broken inference.
- Open a **GitHub issue** with: the file + line, the disputed figure, and a **primary source** (filing,
  regulator, exchange) showing the correct value.
- Or email **resistant@tuta.com** (pseudonymous project channel).
- Every headline figure is meant to be reproducible via `bash run_all.sh`; if a model output and a
  report disagree, that's a bug — please report it.

## Reporting a site/code security issue
- The site is fully static and the poll reads the **public** GitHub API client-side (no tokens, no
  backend). If you find a way it could leak data or be abused, report privately to resistant@tuta.com
  before opening a public issue.

## Scope / non-goals
- Not financial advice. Not a claim of a single conspiracy. Speculative threads are graded and kept
  out of the formal proofs (`spec-*`).
- We will not accept contributions that add personal identifying information or de-anonymize anyone.

## Disclosure
Good-faith reports get credited (pseudonym ok) in the issue thread unless you ask otherwise.
