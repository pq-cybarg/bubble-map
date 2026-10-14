# Blankfein's AI-bubble / 2008-AAA analogy, and the Deaton reply

*Companion to `spec-blankfein-ai-2008-analogy.json`. Records a top-banker primary-source statement that itself draws this project's core analogy - self-marked AI value against AAA mortgage bonds that went to zero - plus a fact-check of the reply's characterizations. Rhetoric is opinion and is not ingested as fact; only checkable claims are graded.*

## The primary source

On 2026-08-22, Lloyd Blankfein (Goldman Sachs CEO 2006-2018) posted, verbatim:

> "Risk management 101 - every exposure should have a limit, even when you're sure nothing could go wrong. After all, the Titanic sank and AAA mortgage bonds went to zero. I worry about the market's (and the economy's) unlimited appetite for exposure to the positive AI revenue story."

This is notable because a former Goldman CEO is drawing the same analogy this corpus maps elsewhere: valuations marked on a self-reinforcing revenue story, like the AAA stamp on subprime bonds that later went to zero. It is carried as a **public_warning** edge from Blankfein to OpenAI (as the stand-in for the AI-revenue story), graded as a top-banker's labeled opinion, not a prediction.

## The reply, fact-checked

John E. Deaton quote-replied the same day, critiquing Blankfein and the 2008 bailout. The underlying bailout and RMBS facts check out; one characterization is corrected:

- **Goldman and TARP** (fact): Treasury injected $10B into Goldman via the TARP Capital Purchase Program on 2008-10-28, enabled by EESA/TARP; Goldman repaid on 2009-06-09, with roughly $1.4B of profit to Treasury (ProPublica Bailout Tracker + Treasury).
- **Goldman and subprime RMBS** (fact): Goldman underwrote and sold subprime RMBS and synthetic CDOs; a 2016 DOJ RMBS settlement of $5.06B and the 2010 SEC Abacus settlement of $550M (incomplete marketing disclosure) are on the record.
- **Who stamped AAA** (correction): the reply's implication that "Goldman stamped AAA" is corrected - **Moody's, S&P, and Fitch assigned the AAA ratings**. This is the ratings-capture point (the issuer-pays rating agencies), modeled as a `stamped_aaa` edge from the rating agencies to the 2007 subprime RMBS, not from Goldman.

## Why it sits in the map

It ties the 2008 ratings-capture mechanism directly to the present AI-financing thread: the same structural question - who marks the value, and who stamps it safe - recurs. See `spec-ai-compute-credit-risk` and `spec-oracle-ai-credit-lynchpin` (the current rating-treatment debate on AI-compute debt) and `macro-history-dereg-manipulation` (the recurring migrate-to-where-the-rule-doesn't-reach pattern).
