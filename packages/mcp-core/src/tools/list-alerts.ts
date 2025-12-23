import { z } from "zod";
import { defineTool } from "../internal/tool-helpers/define";
import { apiServiceFromContext } from "../internal/tool-helpers/api";
import type { ServerContext } from "../types";

export const listAlerts = defineTool({
  name: "list_alerts",
  skills: ["project-management"],
  requiredScopes: ["project:read"],
  description: [
    "List all alert rules for a project in GlitchTip.",
    "Use this tool to see what conditions trigger notifications.",
  ].join("\n"),
  inputSchema: {
    organizationSlug: z
      .string()
      .describe(
        "The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool.",
      ),
    projectSlug: z
      .string()
      .describe(
        "The project's slug. You can find a list of existing projects in an organization using the `find_projects()` tool.",
      ),
  },
  annotations: {
    readOnlyHint: true,
    destructiveHint: false,
    openWorldHint: true,
  },
  async handler(params, context: ServerContext) {
    const apiService = apiServiceFromContext(context);
    const alerts = await apiService.listAlerts(
      params.organizationSlug,
      params.projectSlug,
    );

    if (alerts.length === 0) {
      return `No alert rules found for project ${params.projectSlug}.`;
    }

    let output = `# Alert Rules for ${params.projectSlug}\n\n`;

    for (const alert of alerts) {
      output += `- **${alert.name}**\n`;
      output += `  - ID: ${alert.id}\n`;
      output += `  - Action Match: ${alert.action_match || "all"}\n`;
      output += `  - Frequency: ${alert.frequency || "Default"}\n`;
      output += `  - Created: ${alert.date_created || "Unknown"}\n`;

      if (alert.conditions && alert.conditions.length > 0) {
        output += `  - Conditions: ${alert.conditions.length}\n`;
      }
      if (alert.actions && alert.actions.length > 0) {
        output += `  - Actions: ${alert.actions.length}\n`;
      }
      output += "\n";
    }

    return output;
  },
});
