from __future__ import annotations

from typing import TypedDict


class _Request(TypedDict):
    id: str
    value: float


class Source:
    """
    Represents a source with a name and a list of requests.

    Attributes:
        name (str): The name of the source.
        requests (list): A list of dictionaries representing the requests. Each dictionary has 'id' and 'value' keys.
    """

    def __init__(self, name: str, requests: list[tuple[str, float]]) -> None:
        self.name = name
        self.requests: list[_Request] = [
            {"id": request_id, "value": request_value} for request_id, request_value in requests
        ]

    def total_outflow(self) -> float:
        total = 0.0
        for request in self.requests:
            total += request["value"]
        return total

    def outflow_by_name(self, request_name: str) -> float:
        for request in self.requests:
            if request["id"] == request_name:
                return request["value"]
        return 0.0
