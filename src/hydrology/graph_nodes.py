"""Typed NetworkX node payloads for watershed / flow networks (Phase 2)."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterator
from typing import TYPE_CHECKING, TypeAlias, TypeVar

import networkx as nx

from hydrology.enums import GraphNodeType

if TYPE_CHECKING:
    from hydrology.catchment import Catchment

PAYLOAD_ATTR = "payload"
NODE_TYPE_ATTR = "node_type"

NodePayload: TypeAlias = "CatchmentNode | JunctionNode | SinkNode | SourceNode"
TNodePayload = TypeVar("TNodePayload", bound="CatchmentNode | JunctionNode | SinkNode | SourceNode")


@dataclass
class CatchmentNode:
    """Catchment (runoff source) node in a demand network."""

    node_id: str
    catchment: Catchment | None = None


@dataclass(frozen=True)
class JunctionNode:
    """Junction (flow combination) node in a demand network."""

    node_id: str


@dataclass(frozen=True)
class SinkNode:
    """Outlet / sink node (network discharge point)."""

    node_id: str


@dataclass(frozen=True)
class SourceNode:
    """Synthetic source node feeding the demand network."""

    node_id: str = "source"


def node_type_from_payload(payload: NodePayload) -> GraphNodeType:
    """Map a typed payload to its graph role."""
    if isinstance(payload, CatchmentNode):
        return GraphNodeType.CATCHMENT
    if isinstance(payload, JunctionNode):
        return GraphNodeType.JUNCTION
    if isinstance(payload, SinkNode):
        return GraphNodeType.SINK
    if isinstance(payload, SourceNode):
        return GraphNodeType.SOURCE
    raise TypeError(f"Unexpected payload type: {type(payload)!r}")


def set_node_type(graph: nx.DiGraph, node_id: str, kind: GraphNodeType) -> None:
    """Set ``node_type`` on a graph node (enum stored; GML uses ``kind.value``)."""
    graph.nodes[node_id][NODE_TYPE_ATTR] = kind


def get_node_type(graph: nx.DiGraph, node_id: str) -> GraphNodeType | None:
    """Return parsed ``node_type`` for *node_id*, or ``None`` if unset."""
    data = graph.nodes.get(node_id)
    if data is None:
        return None
    raw = data.get(NODE_TYPE_ATTR)
    if raw is None:
        return None
    return GraphNodeType.from_any(raw)


def _sync_node_type_from_payload(graph: nx.DiGraph, node_id: str, payload: NodePayload) -> None:
    set_node_type(graph, node_id, node_type_from_payload(payload))


def set_node_payload(graph: nx.DiGraph, node_id: str, payload: NodePayload) -> None:
    """Attach a typed payload to ``graph.nodes[node_id]['payload']``."""
    graph.nodes[node_id][PAYLOAD_ATTR] = payload
    _sync_node_type_from_payload(graph, node_id, payload)


def get_node_payload(graph: nx.DiGraph, node_id: str) -> NodePayload | None:
    """Return the typed payload for *node_id*, or ``None`` if unset."""
    data = graph.nodes.get(node_id)
    if data is None:
        return None
    payload = data.get(PAYLOAD_ATTR)
    if payload is None:
        return None
    if not isinstance(payload, (CatchmentNode, JunctionNode, SinkNode, SourceNode)):
        raise TypeError(
            f"Node {node_id!r} payload has unexpected type {type(payload)!r}; "
            "expected CatchmentNode, JunctionNode, SinkNode, or SourceNode"
        )
    return payload


def get_node_payload_or_raise(
    graph: nx.DiGraph,
    node_id: str,
    expected_type: type[TNodePayload],
) -> TNodePayload:
    payload = get_node_payload(graph, node_id)
    if payload is None:
        raise KeyError(f"Node {node_id!r} has no {PAYLOAD_ATTR!r}")
    if not isinstance(payload, expected_type):
        raise TypeError(
            f"Node {node_id!r} payload is {type(payload).__name__}, "
            f"expected {expected_type.__name__}"
        )
    return payload


def attach_payloads_from_node_type(
    graph: nx.DiGraph,
    *,
    source_id: str = "source",
    sink_id: str = "sink",
) -> None:
    """Build payloads on graphs that have ``node_type`` (enum or GML string)."""
    for node_id in graph.nodes:
        if node_id == source_id:
            set_node_payload(graph, node_id, SourceNode(node_id=source_id))
            continue
        if node_id == sink_id:
            set_node_payload(graph, node_id, SinkNode(node_id=sink_id))
            continue
        kind = get_node_type(graph, node_id)
        if kind is GraphNodeType.CATCHMENT:
            from hydrology.catchment import Catchment

            set_node_payload(
                graph,
                node_id,
                CatchmentNode(node_id=str(node_id), catchment=Catchment()),
            )
        elif kind is GraphNodeType.JUNCTION:
            set_node_payload(graph, node_id, JunctionNode(node_id=str(node_id)))
        elif kind is GraphNodeType.SINK:
            set_node_payload(graph, node_id, SinkNode(node_id=str(node_id)))


def iter_catchment_nodes(graph: nx.DiGraph) -> list[CatchmentNode]:
    """All catchment payloads in *graph*."""
    nodes: list[CatchmentNode] = []
    for node_id in graph.nodes:
        payload = get_node_payload(graph, node_id)
        if isinstance(payload, CatchmentNode):
            nodes.append(payload)
    return nodes


def catchment_from_payload(graph: nx.DiGraph, node_id: str) -> Catchment | None:
    """Return the :class:`~hydrology.catchment.Catchment` on a catchment node, if any."""
    payload = get_node_payload(graph, node_id)
    if isinstance(payload, CatchmentNode):
        return payload.catchment
    return None


def require_catchment(graph: nx.DiGraph, node_id: str) -> Catchment:
    """Return the catchment on a catchment node or raise."""
    payload = get_node_payload_or_raise(graph, node_id, CatchmentNode)
    if payload.catchment is None:
        raise ValueError(f"Catchment node {node_id!r} has no catchment instance")
    return payload.catchment


def set_catchment_on_node(graph: nx.DiGraph, node_id: str, catchment: Catchment) -> None:
    """Attach *catchment* to an existing catchment node payload."""
    payload = get_node_payload_or_raise(graph, node_id, CatchmentNode)
    payload.catchment = catchment


def iter_catchment_items(graph: nx.DiGraph) -> Iterator[tuple[str, Catchment]]:
    """Yield ``(node_id, catchment)`` for every catchment node with an instance."""
    for node in iter_catchment_nodes(graph):
        if node.catchment is not None:
            yield node.node_id, node.catchment


def catchments_as_dict(graph: nx.DiGraph) -> dict[str, Catchment]:
    """Snapshot of catchments keyed by node id (for legacy callers)."""
    return dict(iter_catchment_items(graph))
