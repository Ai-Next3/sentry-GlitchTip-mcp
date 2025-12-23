import sys

path = "packages/mcp-core/src/api-client/client.ts"
print(f"Reading {path}")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Define the CLEAN blocks using string concatenation

get_trace_block = """  async getTrace(
    {
      organizationSlug,
      traceId,
      limit = 1000,
      project = "-1",
      statsPeriod = "14d",
    }: {
      organizationSlug: string;
      traceId: string;
      limit?: number;
      project?: string;
      statsPeriod?: string;
    },
    opts?: RequestOptions,
  ): Promise<Trace> {
    const queryParams = new URLSearchParams();
    queryParams.set("limit", String(limit));
    queryParams.set("project", project);
    queryParams.set("statsPeriod", statsPeriod);

    const body = await this.requestJSON(
      "/organizations/" + organizationSlug + "/trace/" + traceId + "/?" + queryParams.toString(),
      undefined,
      opts,
    );
    return TraceSchema.parse(body);
  }"""

search_errors_block = """  async searchErrors(
    {
      organizationSlug,
      projectSlug,
      filename,
      transaction,
      query,
      sortBy = "last_seen",
    }: {
      organizationSlug: string;
      projectSlug?: string;
      filename?: string;
      transaction?: string;
      query?: string;
      sortBy?: "last_seen" | "count";
    },
    opts?: RequestOptions,
  ) {
    const sentryQuery: string[] = [];
    if (filename) {
      sentryQuery.push('stack.filename:"*' + filename.replace(/"/g, '\\\\"') + '"');
    }
    if (transaction) {
      sentryQuery.push('transaction:"' + transaction.replace(/"/g, '\\\\"') + '"');
    }
    if (query) {
      sentryQuery.push(query);
    }
    if (projectSlug) {
      sentryQuery.push("project:" + projectSlug);
    }

    const queryParams = new URLSearchParams();
    queryParams.set("dataset", "errors");
    queryParams.set("per_page", "10");
    queryParams.set(
      "sort",
      "-" + (sortBy === "last_seen" ? "last_seen" : "count"),
    );
    queryParams.set("statsPeriod", "24h");
    queryParams.append("field", "issue");
    queryParams.append("field", "title");
    queryParams.append("field", "project");
    queryParams.append("field", "last_seen()");
    queryParams.append("field", "count()");
    queryParams.set("query", sentryQuery.join(" "));

    const apiUrl = "/organizations/" + organizationSlug + "/events/?" + queryParams.toString();

    const body = await this.requestJSON(apiUrl, undefined, opts);
    return ErrorsSearchResponseSchema.parse(body).data;
  }"""

search_spans_block = """  async searchSpans(
    {
      organizationSlug,
      projectSlug,
      transaction,
      query,
      sortBy = "timestamp",
    }: {
      organizationSlug: string;
      projectSlug?: string;
      transaction?: string;
      query?: string;
      sortBy?: "timestamp" | "duration";
    },
    opts?: RequestOptions,
  ) {
    const sentryQuery: string[] = ["is_transaction:true"];
    if (transaction) {
      sentryQuery.push('transaction:"' + transaction.replace(/"/g, '\\\\"') + '"');
    }
    if (query) {
      sentryQuery.push(query);
    }
    if (projectSlug) {
      sentryQuery.push("project:" + projectSlug);
    }

    const queryParams = new URLSearchParams();
    queryParams.set("dataset", "spans");
    queryParams.set("per_page", "10");
    queryParams.set(
      "sort",
      "-" + (sortBy === "timestamp" ? "timestamp" : "span.duration"),
    );
    queryParams.set("allowAggregateConditions", "0");
    queryParams.set("useRpc", "1");
    queryParams.append("field", "id");
    queryParams.append("field", "trace");
    queryParams.append("field", "span.op");
    queryParams.append("field", "span.description");
    queryParams.append("field", "span.duration");
    queryParams.append("field", "transaction");
    queryParams.append("field", "project");
    queryParams.append("field", "timestamp");
    queryParams.set("query", sentryQuery.join(" "));

    const apiUrl = "/organizations/" + organizationSlug + "/events/?" + queryParams.toString();

    const body = await this.requestJSON(apiUrl, undefined, opts);
    return SpansSearchResponseSchema.parse(body).data;
  }"""

# Locate the gap
start_marker_str = "return IssueSchema.parse(body);\n  }"
start_idx_match = content.find(start_marker_str)

if start_idx_match == -1:
    print("FATAL: Could not find updateIssue end")
    sys.exit(1)

start_idx = start_idx_match + len(start_marker_str)

end_marker_str = (
    "/* -------------------------------------------------------------------------- */"
)
end_idx = content.find(end_marker_str, start_idx)

if end_idx == -1:
    print("FATAL: Could not find Monitors section start")
    sys.exit(1)

print(f"Replacing chunk from {start_idx} to {end_idx}")

# New content
new_chunk = (
    "\n\n"
    + get_trace_block
    + "\n\n"
    + search_errors_block
    + "\n\n"
    + search_spans_block
    + "\n\n  "
)

new_content = content[:start_idx] + new_chunk + content[end_idx:]

with open(path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Restoration complete.")
