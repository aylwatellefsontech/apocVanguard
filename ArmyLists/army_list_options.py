"""Format wargear options for the CSV Options column."""

import re

POWER_RATING = re.compile(r"\(Power Rating ([^)]+)\)", re.IGNORECASE)
WARGEAR_SENTENCE = re.compile(
    r"can (?:also )?(?:be equipped|contain|have)|instead of|must (?:also )?be equipped|"
    r"can include|may be equipped",
    re.IGNORECASE,
)


def _normalize(text):
    return re.sub(r"\s+", " ", text.strip())


def _option_prefix(text):
    lower = text.lower()
    if re.search(r"per weapon|per komb|per model\b", lower):
        m = re.search(r"per (\w+(?: \w+)?)", lower)
        if m:
            return f"per {m.group(1)}"
    for count in (30, 20, 15, 10, 9, 6, 5, 4, 3, 2):
        if re.search(
            rf"every {count} models|for every {count} models|contains {count} models|"
            rf"{count} models|for {count} models|{count} or more models",
            lower,
        ):
            return f"per {count} models"
    return "per Unit"


def _clause_for_match(text, match):
    start = match.start()
    end = match.end()

    boundaries = []
    for sep in (". ", " or ", " - ", "- "):
        pos = text.rfind(sep, 0, start)
        if pos != -1:
            boundaries.append(pos + len(sep))
    clause_start = max(boundaries) if boundaries else 0

    end_boundaries = [len(text)]
    for sep in (". ", " or "):
        pos = text.find(sep, end)
        if pos != -1:
            end_boundaries.append(pos)
    clause_end = min(end_boundaries)

    clause = text[clause_start:clause_end].strip().rstrip(" or").rstrip(",")
    clause = re.sub(r"^[-•]\s*", "", clause)
    return clause


def format_option_entry(text):
    """Return formatted option strings from raw wargear option text."""
    if not text or "Power Rating" not in text:
        return []

    text = _normalize(text)
    entries = []
    seen = set()
    for match in POWER_RATING.finditer(text):
        clause = _clause_for_match(text, match)
        if not clause:
            continue
        pr_value = match.group(1).strip()
        if not pr_value.startswith("+"):
            pr_label = f"Power Rating {pr_value}"
        else:
            pr_label = f"Power Rating {pr_value}"
        prefix = _option_prefix(clause)
        formatted = f"{prefix} ({pr_label}): {clause}"
        if formatted not in seen:
            seen.add(formatted)
            entries.append(formatted)
    return entries


def format_non_pr_entries(text):
    """Return wargear option sentences that have no Power Rating cost."""
    if not text:
        return []

    entries = []
    seen = set()
    for sentence in re.split(r"(?<=[.!?])\s+", _normalize(text)):
        clause = sentence.strip()
        if not clause or "Power Rating" in clause:
            continue
        if not WARGEAR_SENTENCE.search(clause):
            continue
        if not clause.endswith("."):
            clause += "."
        prefix = _option_prefix(clause)
        formatted = f"{prefix}: {clause}"
        if formatted not in seen:
            seen.add(formatted)
            entries.append(formatted)
    return entries


def format_options_from_texts(texts):
    """Combine multiple option blocks into one semicolon-separated Options column value."""
    entries = []
    seen = set()
    for text in texts:
        for entry in format_option_entry(text) + format_non_pr_entries(text):
            if entry not in seen:
                seen.add(entry)
                entries.append(entry)
    return "; ".join(entries)


OPTION_LINE = re.compile(
    r"^per (.+?)(?: \(Power Rating ([^)]+)\))?: (.+)$",
    re.IGNORECASE,
)


def _format_per(per_raw):
    return f"Per {per_raw.strip()}"


def _parse_pt(pr_raw):
    if not pr_raw:
        return None
    match = re.search(r"\+?(\d+)", pr_raw.strip())
    return match.group(1) if match else pr_raw.strip()


def parse_option_line(line):
    """Parse a formatted Options column entry into a JSON option object."""
    line = _normalize(line)
    match = OPTION_LINE.match(line)
    if not match:
        return {"per": "Per Unit", "text": line}

    per_raw, pt_raw, text = match.groups()
    obj = {"per": _format_per(per_raw), "text": text.strip()}
    pt = _parse_pt(pt_raw)
    if pt is not None:
        obj["Pt"] = pt
    return obj


def options_from_text(text):
    """Build option objects from raw wargear option text."""
    formatted = format_option_entry(text) + format_non_pr_entries(text)
    if formatted:
        return [parse_option_line(entry) for entry in formatted]

    text = _normalize(text)
    return [parse_option_line(text)] if text else []


def normalize_options(options):
    """Convert option strings (or mixed input) to JSON option objects."""
    result = []
    for item in options:
        if isinstance(item, dict):
            result.append(item)
        elif isinstance(item, str):
            if re.match(r"^per ", item.strip(), re.IGNORECASE):
                result.append(parse_option_line(item))
            else:
                result.extend(options_from_text(item))
    return result
