import { z } from "zod";
import { defineTool } from "../internal/tool-helpers/define";
import { apiServiceFromContext } from "../internal/tool-helpers/api";
import type { ServerContext } from "../types";

export const createAlert = defineTool({
  name: "create_alert",
  skills: ["project-management"],
  requiredScopes: ["project:write"],
  description: [
    "Create a new alert rule for a project in GlitchTip.",
    "Be careful to specify valid conditions and actions if providing them, otherwise defaults will be used.",
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
    name: z.string().describe("The name of the alert rule."),
    actionMatch: z
      .enum(["all", "any", "none"])
      .optional()
      .describe("When to trigger actions based on conditions. Default: 'all'"),
    frequency: z
      .number()
      .optional()
      .describe("How often to check/alert in minutes. Default: 30"),
  },
  annotations: {
    readOnlyHint: false,
    destructiveHint: false,
    openWorldHint: true,
  },
  async handler(params, context: ServerContext) {
    const apiService = apiServiceFromContext(context);
    const alert = await apiService.createAlert(
      params.organizationSlug,
      params.projectSlug,
      {
        name: params.name,
        actionMatch: params.actionMatch,
        frequency: params.frequency,
      },
    );

    return `Created alert rule "${alert.name}" (ID: ${alert.id}) for project ${params.projectSlug}.`;
  },
});
