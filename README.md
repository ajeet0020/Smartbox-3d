# Box Selection System (Django + DRF)

Recommends the cheapest shipping box that can hold all items of an order.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python manage.py test -v 2     # run tests
```

## Units & assumptions
- Dimensions in **cm**, weight in **kg**, cost in **INR**. Box dimensions are **internal**.
- Items can be rotated in any of 6 orientations. Packing material and box self-weight are ignored.
- Only `is_active=True` boxes are considered.
- v1 recommends a **single box**. If nothing fits, status is `no_box_fits` (multi-box split is future work).

## How a recommendation is made (`shipping/services/packing.py`)
For each active box, checks run cheapest-first:
1. total weight <= `max_weight`
2. total volume <= box volume
3. each item fits alone (sort both sets of dimensions and compare, which handles rotation)
4. a packing heuristic (3D guillotine split, tried with 3 item orderings) places all items

Among boxes that pass, the **lowest cost** wins; ties go to smaller volume, then lower id.
Rejected boxes are returned with a reason.

**Limitation:** 3D bin packing is NP-hard, so step 4 is a heuristic. It never says "fits"
when it doesn't (safe), but may occasionally reject a very tight arrangement that exists.
Orders are capped at 200 units (`MAX_UNITS`).

## API
| Method | URL | Purpose |
|---|---|---|
| CRUD | `/api/products/`, `/api/boxes/`, `/api/orders/` | manage data |
| GET | `/api/orders/{id}/recommend-box/` | recommend for a saved order |
| POST | `/api/recommend-box/` | recommend for ad-hoc items |

```bash
curl -X POST localhost:8000/api/recommend-box/ -H 'Content-Type: application/json' \
  -d '{"items": [{"product_id": 1, "quantity": 2}]}'
```
```json
{"status": "ok", "total_units": 2, "total_weight": 0.8,
 "recommended_box": {"id": 1, "name": "Small", "cost": "20.00"},
 "alternatives": [{"id": 2, "name": "Large", "cost": "45.00"}],
 "volume_utilization": 0.48, "rejected_boxes": []}
```
Invalid input (quantity < 1, empty items, unknown product, non-positive dimensions) returns HTTP 400.

## Tests
`shipping/tests/test_packing.py` (unit, no DB) and `shipping/tests/test_api.py` (API). Output in `TEST_OUTPUT.md`.

## Design decision
The core logic is pure Python with no Django imports, so it is testable on its own. Django/DRF only handle data and HTTP.
