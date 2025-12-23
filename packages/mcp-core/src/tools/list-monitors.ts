import { z } from "zod";
import { defineTool } from "../internal/tool-helpers/define";
import { apiServiceFromContext } from "../internal/tool-helpers/api";
import type { ServerContext } from "../types";

export const listMonitors = defineTool({
  name: "list_monitors",
  skills: ["project-management"],
  requiredScopes: ["org:read"],
  description: [
    "List all uptime monitors for an organization in GlitchTip.",
    "Use this tool to see what websites or services are currently being monitored.",
  ].join("\n"),
  inputSchema: {
    organizationSlug: z
      .string()
      .describe(
        "The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool.",
      ),
  },
  annotations: {
    readOnlyHint: true,
    destructiveHint: false,
    openWorldHint: true,
  },
  async handler(params, context: ServerContext) {
    const apiService = apiServiceFromContext(context);
    const monitors = await apiService.listMonitors(params.organizationSlug);

    if (monitors.length === 0) {
      return "No uptime monitors found for this organization.";
    }

    let output = `# Uptime Monitors for ${params.organizationSlug}\n\n`;

    for (const monitor of monitors) {
      const status =
        monitor.is_up === true
          ? "✅ UP"
          : monitor.is_up === false
            ? "❌ DOWN"
            : "❓ UNKNOWN";
      output += `- **${monitor.name}** (${status})\n`;
      output += `  - URL: ${monitor.url}\n`;
      output += `  - Type: ${monitor.monitor_type}\n`;
      output += `  - Interval: ${monitor.interval}\n`;
      output += `  - Last Check: ${monitor.last_check || "Never"}\n`;
      // Check for project property if it exists in passthrough
      if ((monitor as any).project_name) {
        output += `  - Project: ${(monitor as any).project_name}\n`;
      } else if (monitor.project) {
        output += `  - Project ID: ${monitor.project}\n`;
      }
      output += "\n";
    }

    return output;
  },
});
