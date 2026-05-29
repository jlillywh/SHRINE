"""Allocator priority and delivery (migrated from src/water_manage/test_allocator.py)."""

from __future__ import annotations

import pytest

from water_manage.allocator import Allocator


class TestAllocator:
    def test_priority_order(self, standard_allocator: Allocator) -> None:
        assert standard_allocator.requests[0].name == "evaporation"
        assert standard_allocator.requests[-1].name == "mine"

    def test_change_priority(self, standard_allocator: Allocator) -> None:
        from water_manage.request import Request

        standard_allocator.edit_priority("evaporation", 10)
        standard_allocator.add_request(Request("seepage", 300.0, 1))
        assert standard_allocator.requests[0].name == "seepage"

    def test_supply_setter(self, standard_allocator: Allocator) -> None:
        standard_allocator.supply = 80.0
        assert standard_allocator.total_deliveries() == pytest.approx(80.0)

    def test_add_request(self, standard_allocator: Allocator) -> None:
        from water_manage.request import Request

        name = "environmental"
        amount = 3.65
        standard_allocator.add_request(Request(name, amount, 4))
        assert standard_allocator.get_request(name).amount == amount

    def test_proportional_priority(self, standard_allocator: Allocator) -> None:
        assert standard_allocator.deliveries == {
            "pumping": 10,
            "evaporation": 18,
            "farm": 18,
            "mine": 14,
            "remainder": 0,
        }

    def test_all_equal_priorities(self, standard_allocator: Allocator) -> None:
        standard_allocator.get_request("pumping").amount = 20
        standard_allocator.get_request("mine").priority = 2
        assert standard_allocator.deliveries == {
            "pumping": 11.506849315068493,
            "evaporation": 18,
            "farm": 10.356164383561644,
            "mine": 20.136986301369863,
            "remainder": 0,
        }

    def test_remainder(self, standard_allocator: Allocator) -> None:
        standard_allocator.get_request("pumping").amount = 14.67
        standard_allocator.get_request("mine").amount = 5
        standard_allocator.get_request("mine").priority = 2
        assert standard_allocator.deliveries == {
            "pumping": 14.67,
            "evaporation": 18,
            "farm": 18,
            "mine": 5,
            "remainder": 4.329999999999998,
        }

    def test_default_requests(self) -> None:
        a2 = Allocator()
        assert a2.total_deliveries() == 0.0
        assert a2.requests[0].name == "outflow1"

    @pytest.mark.skip(reason="Legacy test incomplete (no assertion after changing request amount)")
    def test_change_request(self, standard_allocator: Allocator) -> None:
        standard_allocator.requests[0].amount = 17.43
