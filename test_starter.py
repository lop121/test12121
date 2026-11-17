import asyncio
import unittest
from decimal import Decimal

from starter import recommend_price


class RecommendPriceTests(unittest.IsolatedAsyncioTestCase):
    async def test_regular_price_filters_offers_and_rounds_down(self):
        async def fetch_offers():
            return {
                "status": "success",
                "offers": [
                    {"seller": "MyShOp", "price": Decimal("100.00"), "delivery_days": 1},
                    {"seller": "UNKNOWN", "price": Decimal("200.00"), "delivery_days": None},
                    {"seller": "SLOW", "price": Decimal("300.00"), "delivery_days": 7},
                    {"seller": "PARTS", "price": Decimal("4800.01"), "delivery_days": 6},
                    {"seller": "OTHER", "price": Decimal("5100.00"), "delivery_days": 2},
                ],
            }

        result = await recommend_price(
            fetch_offers,
            current_price=Decimal("4900.00"),
            min_price=Decimal("4500.00"),
        )

        self.assertIsInstance(result["price"], Decimal)
        self.assertEqual(result["price"], Decimal("4728.00"))
        self.assertEqual(result["decision"], "APPLY")

    async def test_timeout_keeps_current_price_even_below_minimum(self):
        async def fetch_offers():
            await asyncio.Event().wait()

        result = await recommend_price(
            fetch_offers,
            current_price=Decimal("4000.00"),
            min_price=Decimal("4500.00"),
            timeout_s=0.01,
        )

        self.assertEqual(result["price"], Decimal("4000.00"))
        self.assertEqual(result["decision"], "HOLD")


if __name__ == "__main__":
    unittest.main()
