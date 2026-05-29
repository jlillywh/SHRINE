# Domain contracts (Phase 2)

Typed boundaries for legacy physics under `src/hydrology/` and `src/water_manage/`. The simulation framework (`shrine.simulation`) stays separate; adapters translate between framework context and these contracts.

Related: [modernization-roadmap.md](modernization-roadmap.md) Phase 2, [architecture.md](architecture.md), [ADR 0003 — protocol-based contracts](adr/0003-protocol-based-domain-contracts.md).

## RunoffModel (2.1)

Defined in `hydrology/protocols.py`:

```python
class RunoffModel(Protocol):
    def compute(self, precip: float, et: float) -> Quantity: ...
```

- **Returns:** pint depth rate (e.g. `mm/day` for `Rational`, `m/day` for `Awbm`)
- **Legacy:** objects with `runoff(precip, et) -> float` use `LegacyRunoffAdapter` or `as_runoff_model()`

## Catchment (2.2)

```python
from hydrology.catchment import Catchment, Rational
from hydrology.enums import RunoffMethod

c = Catchment(area=1000.0, runoff_method=RunoffMethod.SIMPLE)  # enum factory
c = Catchment(area=1000.0, runoff_method=Rational())          # or explicit model
volume = c.outflow(precip, et)
```

- **`Catchment.runoff`** — `RunoffModel` instance
- **`Catchment.runoff_method`** — legacy peer (e.g. `Rational` for `.loss` / `.runoff`)
- **`RunoffMethod`** — `SIMPLE`, `AWBM`; `.build()` → `RunoffModel`
- **Deprecated:** bare strings `'simple'` / `'awbm'` emit `DeprecationWarning` (parsed via `RunoffMethod.from_any`)

## Graph node payloads (2.5)

Defined in `hydrology/graph_nodes.py` and stored on each NetworkX node as ``graph.nodes[n]["payload"]``:

| Dataclass | Role |
|-----------|------|
| `CatchmentNode` | Runoff source; optional `catchment` reference |
| `JunctionNode` | Flow junction |
| `SinkNode` | Network outlet |
| `SourceNode` | Synthetic upstream source (`source`) |

Helpers: `set_node_payload`, `get_node_payload`, `get_node_type`, `set_node_type`, `attach_payloads_from_node_type`.

## GraphNodeType (2.7)

Defined in `hydrology/enums.py`:

```python
class GraphNodeType(str, Enum):
    CATCHMENT = "Catchment"
    JUNCTION = "Junction"
    SINK = "Sink"
    SOURCE = "Source"
```

- **`Network.add_catchment` / `add_junction`** store `GraphNodeType` on `graph.nodes[n]["node_type"]`
- **GML I/O** still uses the same string values; `GraphNodeType.from_any()` parses loaded strings
- **`set_node_payload`** keeps `node_type` in sync with the payload dataclass

`water_manage.flow_network.Network.add_catchment` / `add_junction` set payloads automatically; `Watershed.link_catchment` attaches the `Catchment` instance to the payload.

### Catchment registry (2.6)

Catchment objects live **only** on ``CatchmentNode.catchment`` in the graph. Use:

- ``Watershed.get_catchment(node_id)``
- ``Watershed.iter_catchment_items()``

The ``Watershed.catchments`` dict property is deprecated (builds a snapshot from the graph).

## StorageElement (2.4)

Defined in `water_manage/protocols.py`:

```python
class StorageElement(Protocol):
    inflow: float
    request: float
    outflow: float
    overflow: float
    @property
    def quantity(self) -> float: ...
    @property
    def capacity(self) -> float: ...
    def update(self) -> None: ...
```

- **Implementations:** `water_manage.store.Store`, `water_manage.reservoir.Reservoir` (subclass), `tests.conftest.SimpleStore`
- **Simulation:** `shrine.simulation.adapters.reservoir.ReservoirElement` accepts `StorageElement`
- **Alias:** `StorageLike` in `shrine.simulation` is the same protocol (backward-compatible public name)
