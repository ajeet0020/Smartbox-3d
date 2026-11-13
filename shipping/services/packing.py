"""Pure-Python box selection logic (no Django imports).

Units: dimensions in cm, weight in kg. Inputs may be int, float or Decimal.

Design notes
------------
* Rotation: items may be rotated freely in all 6 orientations.
* Packing is a heuristic (guillotine 3D split). It is SOUND: if it says
  "fits", the items really fit. It is not complete: it can occasionally say
  "does not fit" for a very tight arrangement that a perfect packer would find.
  That is the safe direction for a warehouse (never a box that is too small).
"""
from dataclasses import dataclass
from itertools import permutations

MAX_UNITS = 200  # guard: heuristic cost grows with unit count


@dataclass(frozen=True)
class ItemSpec:
    length: object
    width: object
    height: object
    weight: object

    @property
    def dims(self):
        return (self.length, self.width, self.height)

    @property
    def volume(self):
        return self.length * self.width * self.height


@dataclass(frozen=True)
class BoxSpec:
    id: int
    name: str
    length: object
    width: object
    height: object
    max_weight: object
    cost: object

    @property
    def dims(self):
        return (self.length, self.width, self.height)

    @property
    def volume(self):
        return self.length * self.width * self.height


def item_fits_in_box(item_dims, box_dims):
    """One item fits (with rotation) iff sorted dims are each <= sorted box dims."""
    return all(i <= b for i, b in zip(sorted(item_dims), sorted(box_dims)))


def _orientations(dims):
    return set(permutations(dims, 3))


def _try_pack(items, box_dims):
    """Guillotine packing of items (in the given order) into box_dims."""
    spaces = [tuple(box_dims)]
    for item in items:
        best = None  # (space_volume, space_index, orientation)
        for idx, (L, W, H) in enumerate(spaces):
            for (l, w, h) in _orientations(item):
                if l <= L and w <= W and h <= H:
                    vol = L * W * H
                    if best is None or vol < best[0]:
                        best = (vol, idx, (l, w, h))
        if best is None:
            return False
        _, idx, (l, w, h) = best
        L, W, H = spaces.pop(idx)
        # Split leftover into 3 disjoint cuboids.
        for new in ((L - l, w, H), (L, W - w, H), (l, w, H - h)):
            if all(d > 0 for d in new):
                spaces.append(new)
    return True


def can_pack(items, box_dims):
    """items: list of dim-tuples. Tries several orderings; True only if one works."""
    if not all(item_fits_in_box(d, box_dims) for d in items):
        return False
    orderings = (
        sorted(items, key=lambda d: d[0] * d[1] * d[2], reverse=True),
        sorted(items, key=lambda d: max(d), reverse=True),
        sorted(items, key=lambda d: min(d), reverse=True),
    )
    return any(_try_pack(o, box_dims) for o in orderings)


def check_box(units, box):
    """Return (fits: bool, reason: str|None) for a list of ItemSpec units."""
    total_weight = sum(u.weight for u in units)
    if total_weight > box.max_weight:
        return False, "exceeds max weight"
    if sum(u.volume for u in units) > box.volume:
        return False, "exceeds box volume"
    if not all(item_fits_in_box(u.dims, box.dims) for u in units):
        return False, "an item is larger than the box"
    if not can_pack([u.dims for u in units], box.dims):
        return False, "could not be packed"
    return True, None


def recommend_box(order_lines, boxes):
    """order_lines: list of (ItemSpec, quantity). boxes: list of BoxSpec.

    Returns a dict with status 'ok' | 'no_box_fits' | 'too_many_units'
    and, for 'ok', the cheapest fitting box (ties: smaller volume, then id).
    """
    units = [spec for spec, qty in order_lines for _ in range(qty)]
    if not units:
        raise ValueError("order has no items")
    if len(units) > MAX_UNITS:
        return {"status": "too_many_units", "total_units": len(units), "max_units": MAX_UNITS}

    total_weight = sum(u.weight for u in units)
    total_volume = sum(u.volume for u in units)

    fitting, rejected = [], []
    for box in boxes:
        ok, reason = check_box(units, box)
        (fitting if ok else rejected).append((box, reason))

    result = {
        "total_units": len(units),
        "total_weight": total_weight,
        "total_volume": total_volume,
        "rejected": [{"id": b.id, "name": b.name, "reason": r} for b, r in rejected],
    }
    if not fitting:
        result["status"] = "no_box_fits"
        return result

    fitting.sort(key=lambda t: (t[0].cost, t[0].volume, t[0].id))
    best = fitting[0][0]
    result.update(
        status="ok",
        recommended=best,
        alternatives=[b for b, _ in fitting[1:]],
        volume_utilization=float(total_volume / best.volume),
    )
    return result
