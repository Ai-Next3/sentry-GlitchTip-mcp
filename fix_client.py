import sys
import os

path = 'packages/mcp-core/src/api-client/client.ts'
print(f"Reading {path}")

try:
    with open(path, 'r') as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"Error: File not found at {path}")
    sys.exit(1)

new_lines = []
skip = 0
fixed_1 = False
fixed_2 = False

for i, line in enumerate(lines):
    if skip > 0:
        skip -= 1
        continue
    
    # Block 1 detection
    if 'const apiUrl = ` /' in line:
        print(f"Found Block 1 at line {i+1}")
        new_lines.append('    const apiUrl = `/api/0/organizations/${organizationSlug}/issues/${issueId}/events/?${params.toString()}`;\n')
        skip = 8 # Skip next 8 lines
        fixed_1 = True
        continue

    # Block 2 detection
    if '`/api/0/projects/$' in line:
        print(f"Found Block 2 at line {i+1}")
        new_lines.append('      `/api/0/projects/${organizationSlug}/${projectSlug}/events/${eventId}/attachments/`,\n')
        skip = 4 # Skip next 4 lines
        fixed_2 = True
        continue
        
    new_lines.append(line)

if fixed_1 and fixed_2:
    print("Writing fixed content...")
    with open(path, 'w') as f:
        f.writelines(new_lines)
    print("Success!")
else:
    print(f"Failed to find all blocks. Fixed 1: {fixed_1}, Fixed 2: {fixed_2}")
    if not fixed_1:
         # Debug: print context around where block 1 should be
         print("Debug context for Block 1 (around 1759):")
         start = max(0, 1759 - 5)
         end = min(len(lines), 1759 + 5)
         for j in range(start, end):
             print(f"{j+1}: {lines[j].rstrip()}")
