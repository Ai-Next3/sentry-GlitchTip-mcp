import sys

path = "packages/mcp-core/src/api-client/client.ts"
print(f"Reading {path}")

with open(path, "r") as f:
    lines = f.readlines()

# Fix line 1759 (index 1758)
if "const apiUrl =" in lines[1758]:
    print("Fixing line 1759")
    lines[1758] = (
        "    const apiUrl = `/api/0/organizations/${organizationSlug}/issues/${issueId}/events/?${params.toString()}`;\n"
    )
else:
    print(f"WARNING: Line 1759 does not look like apiUrl: {lines[1758]}")

# Fix the attachment line. Search for it.
found = False
for i in range(1770, 1790):
    if "/attachments/" in lines[i]:
        print(f"Fixing attachment line at {i + 1}")
        lines[i] = (
            "      `/api/0/projects/${organizationSlug}/${projectSlug}/events/${eventId}/attachments/`,\n"
        )
        found = True
        break

if not found:
    print("WARNING: Could not find attachment line to fix")

with open(path, "w") as f:
    f.writelines(lines)
print("Done")
