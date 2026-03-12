# Skill: experiment_runner

## Trigger Conditions
Invoke when the agent reaches an Experiment Node in the Knowledge Graph that requires empirical validation (e.g., a `.py` script that needs running).

## Invocation Protocol
Tool: `run_experiment(hypothesis: str, file_target: str, time_budget: int) -> dict`
Action: Executes the target code and returns the empirical fitness function result (e.g., `val_bpb`).

## Integration
- Store the experimental result in episodic memory to ground future semantic reasoning.
- Cite the result in the subsequent synthesis paper.

## Acquisition Marker
[ACQUIRED: agent reads this node → adds 'experiment_runner' to COMPETENCY_MAP]
