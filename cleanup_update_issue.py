import sys

path = "packages/mcp-core/src/api-client/client.ts"
print(f"Reading {path}")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Define the CLEAN block for updateIssue using string concatenation
clean_block = """  async updateIssue(
    {
      organizationSlug,
      issueId,
      status,
      assignedTo,
    }: {
      organizationSlug: string;
      issueId: string;
      status?: string;
      assignedTo?: string;
    },
    opts?: RequestOptions,
  ): Promise<Issue> {
    const updateData: Record<string, any> = {};
    if (status !== undefined) updateData.status = status;
    if (assignedTo !== undefined) updateData.assignedTo = assignedTo;

    const body = await this.requestJSON(
      "/api/0/organizations/" + organizationSlug + "/issues/" + issueId + "/",
      {
        method: "PUT",
        body: JSON.stringify(updateData),
      },
      opts,
    );
    return IssueSchema.parse(body);
  }"""

# Find start of updateIssue
start_marker = "async updateIssue("
# Find end of updateIssue. It ends before `// TODO:` or `async getTrace` (commented out) or `async listMonitors`?
# Let's search for the NEXT method start.
# Scanning the file content, what comes after?
# In view_file 1873: // TODO: Sentry is not yet exposing...
# In view_file 1899: // async getTrace...

# I'll just find the matching closing brace? No too hard with regex or simple find.
# I will assume `// TODO: Sentry is not yet exposing` is the boundary.
end_marker = "// TODO: Sentry is not yet exposing"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1:
    print("FATAL: Could not find updateIssue start")
    sys.exit(1)
if end_idx == -1:
    print("FATAL: Could not find end marker (TODO comment)")
    # Fallback: look for `async listMonitors`? Or whatever is next.
    # Let's try to print the text around start_idx + 500
    print("End marker not found. Text context:")
    print(content[start_idx : start_idx + 600])
    sys.exit(1)

print(f"Replacing chunk from {start_idx} to {end_idx}")

new_content = content[:start_idx] + clean_block + "\n\n  " + content[end_idx:]

with open(path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("UpdateIssue cleanup complete.")
