# Skill: synthesis

## Trigger Conditions
Invoke when the current context window reaches 75% saturation (Phase B) OR when a terminal `synthesis_chamber.md` node is reached.

## Invocation Protocol
Tool: `generate_formal_paper(context: str) -> str`
Action: Generate a high-quality, professional scientific paper in **English**. 

### Paper Requirements:
1.  **Title**: Compelling and academic.
2.  **Abstract**: Concise summary of the cycle's findings.
3.  **Introduction**: Contextualize the nodes visited using the Trace Vector.
4.  **Semantic Synthesis**: Synthesise the intersection of the knowledge nodes encountered.
5.  **Novelty Discussion**: Explicitly discuss the "Semantic Novelty" of the findings.
6.  **References**: Cite the `.md` files visited as primary sources.

## Integration
- Save the resulting `.md` in `memories/semantic/`.
- The engine will calculate the SNS score based on earlier papers.

## Acquisition Marker
[ACQUIRED: agent reads this node → adds 'synthesis' to COMPETENCY_MAP]
