# Step debugging API (RUN-04)

Use `RunController` in **step mode** to advance one timestep at a time, inspect inputs and mass balance, then collect outputs with `complete()`.

## Workflow

### Context manager (recommended)

```python
from shrine.simulation import RunController, RunSession

controller = RunController(model, input_manager=inputs, seed=42)

with RunSession(controller) as session:  # or: with controller.session() as session:
    for step in session:
        print(step.current_time, step.inputs, step.balance)

result = session.result  # RunResult after the block exits
```

### Manual stepping

```python
controller = RunController(model, input_manager=inputs, seed=42)
controller.reset()  # fresh clock + recorder

while (step := controller.step()) is not None:
    print(step.current_time, step.inputs, step.balance)

result = controller.complete()  # finalize elements, return DataFrame
```

Alternatively call `begin()` to run `initialize` hooks without advancing time, then `step()`.

## `StepResult` fields

| Field | Description |
|-------|-------------|
| `step_index` | Timestep index before clock advance |
| `current_time` | Simulation timestamp for this step |
| `inputs` | Bound input values for this timestep |
| `timestep_context` | Full context passed to elements |
| `balance` | `MassBalanceReport` when elements contribute balance terms |
| `done` | `True` if the clock reached `end_date` after this step |
| `passed` | Mass balance passed (or no terms to check) |

## Helpers

- `step_many(n)` — advance up to `n` steps
- `is_running`, `is_initialized`, `steps_completed`, `last_step` — session state
- `reset()` — reset clock/recorder for a new session
- `RunSession` / `controller.session()` — `with` block runs `begin()` on enter, `complete()` on clean exit, `finalize()` on exception (1.5)
- `finalize()` — call element finalize hooks without building `RunResult`
- `complete()` — finalize and return `RunResult` with `metadata["debug_mode"] = True`

## Notes

- After a full `run()`, call `reset()` before stepping again (the clock is at `end_date`).
- Mass balance failures fail-fast on `step()` when `verify_mass_balance=True` (default).
- Example script: `examples/step_debug.py`
