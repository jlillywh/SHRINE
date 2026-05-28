import warnings

import networkx as nx

from hydrology.catchment import Catchment
from hydrology.enums import GraphNodeType
from hydrology.graph_nodes import (
    CatchmentNode,
    catchments_as_dict,
    get_node_type,
    iter_catchment_items,
    require_catchment,
    set_node_payload,
)
from water_manage.flow_network import Network


class Watershed(Network):
    """Watershed demand network of catchments and junctions.

    Catchment instances are stored on graph node payloads (``CatchmentNode`` on
    ``self.dg``), not in a separate registry. Use :meth:`get_catchment` or
    :meth:`iter_catchment_items` to access them.
    """

    def __init__(self) -> None:
        Network.__init__(self)

    def link_catchment(
        self,
        name: str,
        downstream_name: str = "sink",
        *,
        catchment: Catchment | None = None,
    ) -> Catchment:
        """Add a catchment node and attach a :class:`~hydrology.catchment.Catchment`."""
        self.add_catchment(name, downstream_name)
        instance = catchment if catchment is not None else Catchment()
        set_node_payload(
            self.dg,
            name,
            CatchmentNode(node_id=name, catchment=instance),
        )
        return instance

    def iter_catchment_items(self):
        """Yield ``(node_id, catchment)`` from graph payloads."""
        return iter_catchment_items(self.dg)

    def get_catchment(self, catchment_name: str) -> Catchment:
        """Return the catchment registered on *catchment_name*."""
        return require_catchment(self.dg, catchment_name)

    @property
    def catchments(self) -> dict[str, Catchment]:
        """Deprecated: catchments now live on graph node payloads."""
        warnings.warn(
            "Watershed.catchments is deprecated; use get_catchment(), "
            "iter_catchment_items(), or CatchmentNode payloads on self.dg.",
            DeprecationWarning,
            stacklevel=2,
        )
        return catchments_as_dict(self.dg)

    def discharge(self, precip: float, et: float) -> float:
        """Route catchment runoff through the network and return outlet flow."""
        for name, catchment in iter_catchment_items(self.dg):
            self.update_capacity(name, catchment.outflow(precip, et))
        return self.outflow()

    def delete_node(self, node_name: str) -> None:
        sub = nx.bfs_tree(self.dg, source=node_name, reverse=True)
        for node in list(sub.nodes):
            self.dg.remove_node(node)

    def set_outflow_node(self, junct_name: str) -> None:
        """Assign the junction that receives total watershed discharge."""
        self.sink = junct_name

    def get_node(self, node_name: str):
        """Return raw NetworkX node data for *node_name*."""
        try:
            return self.dg.nodes[node_name]
        except KeyError:
            print(f"The node {node_name} does not exist!")
            return None

    def load_from_file(self, filename: str) -> None:
        from hydrology.graph_nodes import attach_payloads_from_node_type

        self.dg = nx.read_gml(filename)
        for node in self.dg.copy().nodes():
            try:
                if get_node_type(self.dg, node) is GraphNodeType.CATCHMENT:
                    self.dg.add_edge(self.source, node)
            except KeyError:
                pass
        attach_payloads_from_node_type(
            self.dg,
            source_id=self.source,
            sink_id=self.sink,
        )
