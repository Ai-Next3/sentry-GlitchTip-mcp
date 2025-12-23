import sys

path = "packages/mcp-core/src/api-client/client.ts"
print(f"Reading {path}")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()


# Helper to replace using string concatenation
def to_concat(tpl):
    # This is a naive helper, I'll just write the blocks manually for safety.
    pass


# BLOCK 1: searchErrors
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

# BLOCK 2: searchSpans (replacing template literals with concat)
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

# BLOCK 3: getTrace (replacing template literals)
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

# Replacements logic
# searchErrors
start_search_errors = content.find("async searchErrors(")
end_search_errors = content.find("async searchSpans(")
if start_search_errors != -1 and end_search_errors != -1:
    print("Replacing searchErrors")
    content = (
        content[:start_search_errors]
        + search_errors_block
        + "\n\n"
        + content[end_search_errors:]
    )

# searchSpans
start_spans = content.find("async searchSpans(")
end_spans = content.find(
    "/* -------------------------------------------------------------------------- */"
)  # API QUERY BUILDERS section separator?
# Actually, looking at file, there is a separator after searchSpans?
# Line 1993: // =================...
separator = "// ================================================================================"
end_spans = content.find(separator)

if start_spans != -1 and end_spans != -1:
    print("Replacing searchSpans")
    content = (
        content[:start_spans] + search_spans_block + "\n\n  " + content[end_spans:]
    )

# getTrace
start_trace = content.find("async getTrace(")
end_trace = content.find(
    "/* -------------------------------------------------------------------------- */",
    start_trace,
)  # Section separator for Monitors
# Monitors section starts at line 2364

if start_trace != -1 and end_trace != -1:
    print("Replacing getTrace")
    content = content[:start_trace] + get_trace_block + "\n\n  " + content[end_trace:]

# Monitors (listMonitors, createMonitor)
# I will just replace valid methods with Concat versions at the end of the file.
# First, I'll truncate the file before "async listMonitors"
start_monitors = content.find("async listMonitors(")
if start_monitors != -1:
    print("Replacing Monitors section")
    content = content[:start_monitors]  # Truncate

    # Append new monitor methods + Status Page methods
    new_methods = """  async listMonitors(
    organizationSlug: string,
    opts?: RequestOptions,
  ): Promise<MonitorList> {
    const body = await this.requestJSON(
      "/organizations/" + organizationSlug + "/monitors/",
      undefined,
      opts,
    );
    return MonitorListSchema.parse(body);
  }

  async createMonitor(
    organizationSlug: string,
    data: {
      name: string;
      url: string;
      monitorType: string;
      interval: string;
      project?: string | number;
    },
    opts?: RequestOptions,
  ): Promise<Monitor> {
    const payload = {
      name: data.name,
      url: data.url,
      monitor_type: data.monitorType,
      interval: data.interval,
      project: data.project,
    };

    const body = await this.requestJSON(
      "/organizations/" + organizationSlug + "/monitors/",
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
      opts,
    );
    return MonitorSchema.parse(body);
  }

  async listStatusPages(
    organizationSlug: string,
    opts?: RequestOptions,
  ): Promise<StatusPageList> {
    const body = await this.requestJSON(
      "/organizations/" + organizationSlug + "/status-pages/",
      undefined,
      opts,
    );
    return StatusPageListSchema.parse(body);
  }

  async createStatusPage(
    organizationSlug: string,
    data: {
      name: string;
      slug: string;
      is_public?: boolean;
      domain?: string;
    },
    opts?: RequestOptions,
  ): Promise<StatusPage> {
    const payload = {
      name: data.name,
      slug: data.slug,
      is_public: data.is_public ?? true,
      domain: data.domain,
    };

    const body = await this.requestJSON(
      "/organizations/" + organizationSlug + "/status-pages/",
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
      opts,
    );
    return StatusPageSchema.parse(body);
  }
}
"""
    content += new_methods

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Final cleanup complete.")
