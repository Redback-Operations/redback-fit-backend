import hashlib, os, re, uuid
from datetime import date

# Optional salts for extra safety; we can add to a .env later
PII_SALT   = os.getenv("PII_SALT", "")
PII_PEPPER = os.getenv("PII_PEPPER", "")

def stable_hash(value: str | None) -> str | None:
    """Deterministic, non-reversible hash for identifiers like email."""
    if not value:
        return None
    data = (PII_SALT + value + PII_PEPPER).encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def initials(full_name: str | None) -> str | None:
    """J D for 'Jane Doe'. Up to 3 initials, letters only."""
    if not full_name:
        return None
    parts = re.findall(r"[A-Za-z]+", full_name)
    return "".join(p[0].upper() for p in parts[:3]) or None

def pseudonym(namespace: str, raw_key: str) -> str:
    """Stable pseudonym like user_7f3ab2 derived from a namespace + raw key."""
    ns = uuid.uuid5(uuid.NAMESPACE_URL, namespace)
    return "user_" + uuid.uuid5(ns, raw_key).hex[:8]

def birth_year_from_iso(dob_iso: str | None) -> int | None:
    """YYYY[-MM[-DD]] -> YYYY"""
    try:
        return int(dob_iso[:4]) if dob_iso else None
    except Exception:
        return None

def age_bucket_from_year(year: int | None) -> str | None:
    """Return coarse age bucket for privacy (e.g., 18-24, 25-29, 30-34, ..., 50+)."""
    if not year:
        return None
    today_year = date.today().year
    age = max(0, today_year - year)
    bins = [(0,17),(18,24),(25,29),(30,34),(35,39),(40,44),(45,49),(50,120)]
    for lo, hi in bins:
        if lo <= age <= hi:
            return f"{lo:02d}-{hi:02d}" if hi < 120 else f"{lo:02d}+"
    return None
