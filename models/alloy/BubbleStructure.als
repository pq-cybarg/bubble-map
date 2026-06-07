/*
 * BubbleStructure.als - relational/structural model of the AI circular-funding graph.
 * Value-flow edge x->y means x sends value to y (equity, compute payment, or GPU purchase).
 * Edges are the documented relationships in data/graph.json.
 *
 * Checks (a `check` reports a COUNTEREXAMPLE if the assertion is false;
 *         "unsatisfiable / no counterexample" means the assertion HOLDS for this graph):
 *   CoreIsCircular                    - OpenAI/NVIDIA/Oracle/CoreWeave each lie on a cycle (HOLDS)
 *   SpaceXCircular_WithCancelable     - SpaceX lies on a cycle when cancelable edges count (HOLDS)
 *   SpaceXSeparable_WithoutCancelable - SpaceX is NOT on any cycle once cancelable edges are removed (HOLDS)
 */
module BubbleStructure

abstract sig Entity { flow: set Entity }
one sig NVIDIA, OpenAI, Oracle, CoreWeave, Microsoft, Amazon, Anthropic, Google, SpaceX, Banks extends Entity {}

fact Edges {
  flow =
      NVIDIA->OpenAI    + OpenAI->NVIDIA
    + NVIDIA->CoreWeave + CoreWeave->NVIDIA
    + OpenAI->Oracle    + Oracle->NVIDIA
    + OpenAI->CoreWeave
    + Microsoft->OpenAI + OpenAI->Microsoft
    + Amazon->Anthropic + Anthropic->Amazon
    + NVIDIA->Anthropic
    + Google->Anthropic
    + Google->SpaceX                       // cancelable
    + Anthropic->SpaceX                     // cancelable
    + SpaceX->NVIDIA                        // cancelable
    + CoreWeave->Banks  + Oracle->Banks
}

fun cancelable : Entity->Entity {
  Google->SpaceX + Anthropic->SpaceX + SpaceX->NVIDIA
}

pred onCycle[e: Entity]            { e in e.^flow }
pred onCycleRobust[e: Entity]      { e in e.^(flow - cancelable) }

assert CoreIsCircular {
  onCycle[OpenAI] and onCycle[NVIDIA] and onCycle[Oracle] and onCycle[CoreWeave]
}
assert SpaceXCircular_WithCancelable      { onCycle[SpaceX] }
assert SpaceXSeparable_WithoutCancelable  { not onCycleRobust[SpaceX] }

// Also: the core remains circular even without cancelable edges (robust core).
assert CoreCircular_Robust {
  onCycleRobust[OpenAI] and onCycleRobust[NVIDIA] and onCycleRobust[Oracle] and onCycleRobust[CoreWeave]
}

check CoreIsCircular for 10
check SpaceXCircular_WithCancelable for 10
check SpaceXSeparable_WithoutCancelable for 10
check CoreCircular_Robust for 10
