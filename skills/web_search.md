# Skill: web_search

## Trigger Conditions
Invoke when the current knowledge node lacks sufficient evidence, or when a factual claim requires external verification that is not present in the graph.

## Invocation Protocol
Tool: `web_search(query: str) -> List[Result]`
Action: Retrieves real-time data from the open web.

## Integration
Store results as ephemeral context. Cite sources in the final synthesis.

## Acquisition Marker
[ACQUIRED: agent reads this node → adds 'web_search' to COMPETENCY_MAP]
