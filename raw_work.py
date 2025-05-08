import re

def parse_expression(expr):
    # Regex: First side contains caddr, second side does not
    pattern = re.compile(
        r"""
        \[([LR]):\s*\(([\w\s,]+),\s*caddr\),\s*      # group(1): original side
        ([LR]):\s*\(([\w\s,]+)\),\s*                 # group(3): replacement side
        Case:\s*(\w+)\]                              # group(5): case version
        """, re.VERBOSE
    )

    match = pattern.match(expr)
    if not match:
        return None

    original_label = match.group(1)
    original_versions_raw = match.group(2)
    replacement_label = match.group(3)
    replacement_versions_raw = match.group(4)
    case_version = match.group(5)

    original_versions = [v.strip() for v in original_versions_raw.split(',') if v.strip()]
    replacement_versions = [v.strip() for v in replacement_versions_raw.split(',') if v.strip()]

    side = "left" if original_label == "L" else "right"

    # Handle original: 1 or 2 versions before caddr
    if len(original_versions) == 2:
        original_device = original_versions[0]
        original_device_pending = original_versions[1]
    else:
        original_device = original_versions[0]
        original_device_pending = None

    replacement_device = replacement_versions[0]

    return {
        "original_device": original_device,
        "original_device_pending": original_device_pending,
        "replacement_device": replacement_device,
        "case_version": case_version,
        "side": side
    }

# ✅ Example usage:
expr1 = "[L: (2A142, caddr), R: (2A144), Case: 2A146]"
expr2 = "[R: (2A144, 2A143, caddr), L: (2A142), Case: 2A146]"

print(parse_expression(expr1))
print(parse_expression(expr2))
