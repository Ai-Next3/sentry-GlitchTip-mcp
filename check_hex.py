import sys

path = "packages/mcp-core/src/api-client/client.ts"
print(f"Reading {path}")

with open(path, "rb") as f:
    lines = f.readlines()
    if len(lines) > 1758:
        line = lines[1758]
        print(f"Content: {line}")
        print(f"Hex: {line.hex()}")
    else:
        print("Line 1759 not found")
