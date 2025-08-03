from tests.base_test import DBTestCase
from app.models.production import insert_production, fetch_production
from app.utils.simulator import simulate_production_dates

class TestProduction(DBTestCase):
    def test_insert_and_fetch_production(self):
        dummy_image = b'\x89PNG\r\n'
        produced_on, dispatched_on = simulate_production_dates()
        insert_production("TEST124", "2026-01-01 00:00:00", dummy_image, produced_on, dispatched_on)
        productions = fetch_production()
        self.assertTrue(any(p["ID No"] == "124" for p in productions))
