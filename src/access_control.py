from __future__ import annotations

import os


def parse_allowed_ids(variable_name: str) -> frozenset[int]:
    raw_value = os.getenv(variable_name, "")
    result: set[int] = set()
    for item in raw_value.split(","):
        value = item.strip()
        if not value:
            continue
        try:
            account_id = int(value)
        except ValueError:
            continue
        if account_id > 0:
            result.add(account_id)
    return frozenset(result)


def is_allowed(account_id: int | None, allowed_ids: frozenset[int]) -> bool:
    return account_id is not None and account_id in allowed_ids
