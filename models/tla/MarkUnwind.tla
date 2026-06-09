---------------------------- MODULE MarkUnwind ----------------------------
(***************************************************************************)
(* Temporal model of the AI PAPER-MARKS unwind - the EARNINGS-side        *)
(* analogue of BubbleCascade (which models the CASH default cascade).     *)
(*                                                                         *)
(* Hyperscalers carry private-lab stakes at self-set marks                *)
(* (models/z3/reflexive_marks.py, M2a). A single exogenous shock - a      *)
(* down-round or an IPO that clears BELOW the last private mark (M3) -      *)
(* forces fair-value holders (Amazon, Google) to REVERSE their booked     *)
(* gains. The reported-earnings hit pulls capex (M4), which keeps the      *)
(* labs unfunded -> the reflexive loop closes.                            *)
(*                                                                         *)
(* Inv_MarksHold is EXPECTED TO BE VIOLATED: TLC returns the explicit     *)
(* writedown trace = the step-by-step paper-marks reversal.               *)
(***************************************************************************)
EXTENDS FiniteSets

FairValueHolders == {"Amazon","Google"}   \* carry Anthropic at FAIR VALUE (book gains)
Labs == {"Anthropic","OpenAI"}            \* Microsoft holds OpenAI at equity method (books losses already)

VARIABLES round, mark, lab, capex
vars == <<round, mark, lab, capex>>

TypeOK == /\ round \in {"flow","stop"}
          /\ mark  \in [FairValueHolders -> {"up","down"}]
          /\ lab   \in [Labs -> {"funded","unfunded"}]
          /\ capex \in {"high","cut"}

Init == /\ round = "flow"
        /\ mark  = [h \in FairValueHolders |-> "up"]
        /\ lab   = [l \in Labs |-> "funded"]
        /\ capex = "high"

\* Exogenous trigger: a down-round / IPO clears BELOW the last private mark.
Shock == round = "flow" /\ round' = "stop" /\ UNCHANGED <<mark, lab, capex>>

\* Once the round fails, a lab can no longer be marked/funded at the higher valuation.
LabUnfund(l) == round = "stop" /\ lab[l] = "funded"
                /\ lab' = [lab EXCEPT ![l] = "unfunded"]
                /\ UNCHANGED <<round, mark, capex>>

\* Fair-value holders MUST write down once Anthropic is unfunded (M3: forced reversal).
MarkDown(h) == h \in FairValueHolders /\ mark[h] = "up" /\ lab["Anthropic"] = "unfunded"
               /\ mark' = [mark EXCEPT ![h] = "down"]
               /\ UNCHANGED <<round, lab, capex>>

\* Reflexive feedback (M4): once any mark reverses, the earnings hit pulls capex,
\* which keeps the labs unfunded -> the loop closes.
CapexCut == capex = "high" /\ (\E h \in FairValueHolders : mark[h] = "down")
            /\ capex' = "cut" /\ UNCHANGED <<round, mark, lab>>

Next == \/ Shock
        \/ \E l \in Labs : LabUnfund(l)
        \/ \E h \in FairValueHolders : MarkDown(h)
        \/ CapexCut
        \/ UNCHANGED vars

Spec == Init /\ [][Next]_vars

(***************************************************************************)
(* EXPECTED TO BE VIOLATED -> the violation trace IS the writedown cascade *)
(* (round stops -> Anthropic unfunded -> Amazon & Google reverse marks).   *)
(***************************************************************************)
Inv_MarksHold == ~(mark["Amazon"] = "down" /\ mark["Google"] = "down")
=============================================================================
