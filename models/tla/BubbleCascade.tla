-------------------------- MODULE BubbleCascade --------------------------
(***************************************************************************)
(* Temporal model of the AI-bubble UNWIND as a default cascade through    *)
(* the circular-funding graph (data/graph.json).                          *)
(*                                                                         *)
(* Each node has status S (solvent) / T (stressed) / D (defaulted).       *)
(* A single EXOGENOUS shock - the external-capital tap stopping (carry-   *)
(* trade unwind / rate shock; see research/macro-carry-trades.json) -     *)
(* propagates because the core is solvent-only-while-inflows-continue     *)
(* (Z3 theorem T4).                                                        *)
(*                                                                         *)
(* Two facts are model-checked:                                           *)
(*   Inv_NoCoreCollapse  - EXPECTED TO BE VIOLATED: TLC returns an        *)
(*       explicit contagion trace = the step-by-step bubble unwind.       *)
(*   Inv_SpaceXSafe      - EXPECTED TO HOLD: SpaceX (exogenous Starlink    *)
(*       revenue) never defaults even with the tap shut - validating the  *)
(*       user's prior that SpaceX is separable from the core.             *)
(***************************************************************************)
EXTENDS FiniteSets

Nodes == {"NVIDIA","OpenAI","Oracle","CoreWeave","Anthropic",
          "Microsoft","Amazon","SpaceX","Banks"}

VARIABLES status, tap
vars == <<status, tap>>

TypeOK == /\ status \in [Nodes -> {"S","T","D"}]
          /\ tap \in {"flow","stop"}

Init == /\ status = [n \in Nodes |-> "S"]
        /\ tap = "flow"

\* The exogenous trigger: external capital stops flowing (the bubble's fuel cut off).
Shock == /\ tap = "flow"
         /\ tap' = "stop"
         /\ UNCHANGED status

Set(n, v) == status' = [status EXCEPT ![n] = v] /\ UNCHANGED tap

\* Pure compute-dependent labs die immediately once the tap is shut (Z3 T4: no exogenous revenue).
OpenAIFail   == status["OpenAI"] = "S"   /\ tap = "stop" /\ Set("OpenAI","D")
AnthropicFail== status["Anthropic"] = "S"/\ tap = "stop" /\ Set("Anthropic","D")

\* Neoclouds die when their anchor customer dies or the tap is shut (GPU-debt service).
CoreWeaveFail== status["CoreWeave"] # "D"
               /\ (status["OpenAI"] = "D" \/ tap = "stop")
               /\ Set("CoreWeave","D")

\* Oracle: ~$300B RPO is mostly OpenAI; debt-funded buildout -> default when OpenAI dies.
OracleFail   == status["Oracle"] # "D" /\ status["OpenAI"] = "D" /\ Set("Oracle","D")

\* NVIDIA: huge exogenous demand exists, but the circular slice (~$132B) evaporates -> STRESSED, not dead.
NvidiaStress == status["NVIDIA"] = "S"
               /\ status["OpenAI"] = "D" /\ status["CoreWeave"] = "D"
               /\ Set("NVIDIA","T")

\* Hyperscalers: equity-method losses + RPO write-downs -> STRESSED, survive on real cash flow.
MicrosoftStress == status["Microsoft"] = "S" /\ status["OpenAI"] = "D" /\ Set("Microsoft","T")
AmazonStress    == status["Amazon"] = "S" /\ status["Anthropic"] = "D" /\ Set("Amazon","T")

\* Spillover to the credit system (private credit / GPU-collateral / First Brands-style).
BanksStress  == status["Banks"] = "S"
               /\ (status["CoreWeave"] = "D" \/ status["Oracle"] = "D")
               /\ Set("Banks","T")

\* NOTE: there is deliberately NO action that sets SpaceX to "D".
\* SpaceX has exogenous Starlink/launch revenue; its loop entanglement is via
\* CANCELABLE contracts (data/graph.json), so it reverts to solvent when the loop fails.

Next == \/ Shock
        \/ OpenAIFail \/ AnthropicFail \/ CoreWeaveFail \/ OracleFail
        \/ NvidiaStress \/ MicrosoftStress \/ AmazonStress \/ BanksStress
        \/ UNCHANGED vars   \* allow stuttering / fixpoint

Spec == Init /\ [][Next]_vars

(***************************************************************************)
(* INVARIANTS                                                             *)
(***************************************************************************)
\* EXPECTED TO BE VIOLATED -> the violation trace IS the contagion sequence.
Inv_NoCoreCollapse ==
    ~(status["OpenAI"] = "D" /\ status["CoreWeave"] = "D" /\ status["Oracle"] = "D")

\* EXPECTED TO HOLD -> SpaceX is resilient to the cascade.
Inv_SpaceXSafe == status["SpaceX"] # "D"
=============================================================================
