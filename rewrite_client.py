import sys
import re

path = "packages/mcp-core/src/api-client/client.ts"
print(f"Reading {path}")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Define the CLEAN replacement for listEventsForIssue
method_replacement = """  async listEventsForIssue(
    {
      organizationSlug,
      issueId,
      query,
      limit = 50,
      sort,
      statsPeriod,
      start,
      end,
      full = false,
    }: {
      organizationSlug: string;
      issueId: string;
      query?: string;
      limit?: number;
      sort?: string;
      statsPeriod?: string;
      start?: string;
      end?: string;
      full?: boolean;
    },
    opts?: RequestOptions,
  ) {
    const params = new URLSearchParams();

    if (query) {
      params.append("query", query);
    }

    params.append("per_page", String(limit));

    if (sort) {
      params.append("sort", sort);
    }

    if (statsPeriod) {
      params.append("statsPeriod", statsPeriod);
    } else if (start && end) {
      params.append("start", start);
      params.append("end", end);
    }

    if (full) {
      params.append("full", "true");
    }

    const apiUrl = `/api/0/organizations/${organizationSlug}/issues/${issueId}/events/?${params.toString()}`;
    return await this.requestJSON(apiUrl, undefined, opts);
  }"""

# Regex to find the broken method. It starts at `async listEventsForIssue` and ends before `async listEventAttachments`.
# Since the body is mangled, we search for the start and the start of the NEXT method.
pattern = r"async listEventsForIssue\s*\(.*?\)\s*\{.*?return await this\.requestJSON\(apiUrl, undefined, opts\);\s*\}"
# This regex is hard because of the mangled body.

# Alternative: Find start index and end index physically.
start_marker = "async listEventsForIssue("
end_marker = "async listEventAttachments("

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("FATAL: Could not find method boundaries.")
    sys.exit(1)

print(f"Replacing chunk from {start_idx} to {end_idx}")
# The replacement should not include the end_marker itself.
# We also need to preserve whitespace before start_marker?
# The replacement string includes correct indentation.

# Read the indentation of the start marker line
last_newline = content.rfind("\n", 0, start_idx)
indentation = content[last_newline + 1 : start_idx]

# Check if content needs replacement at all (maybe it's already "fixed" but with weird chars)
# We will blindly replace it.

new_content = content[:start_idx] + method_replacement + "\n\n  " + content[end_idx:]

# Also fix the second method `listEventAttachments` URL manually in the new content
# Pattern: `/api/0/projects/$...`
# We use simple string replace for the unique URL part if it exists in expected bad form
bad_url_part = "`/api/0/projects/$"  # Just checking if it's there
if bad_url_part in new_content:
    # Actually, if we use the same technique for the second method:
    pass

# Let's just fix the second method URL specificly by finding it in new_content
# It's inside listEventAttachments
start_attach = new_content.find("async listEventAttachments(")
if start_attach != -1:
    # Look for the return await body part
    # We expected:
    # const body = await this.requestJSON(
    #   `/api/0/projects/${organizationSlug}/${projectSlug}/events/${eventId}/attachments/`,
    #   undefined,
    #   opts,
    # );

    # We will search for `const body = await this.requestJSON(` and replace the literal argument.
    # This is slightly risky if multiple exist.
    # But we know it is inside listEventAttachments.

    # Let's simply replace the KNOWN BAD STRING if it exists.
    # Or just replace the line that contains `/attachments/`

    # Split to lines for safe line-by-line editing of the rest
    lines = new_content.split("\n")
    for i, line in enumerate(lines):
        if (
            "/attachments/" in line and "requestJSON" not in line
        ):  # It's the arguments line
            # Force overwrite it
            lines[i] = (
                "      `/api/0/projects/${organizationSlug}/${projectSlug}/events/${eventId}/attachments/`,"
            )

    new_content = "\n".join(lines)

with open(path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Rewrite complete.")
