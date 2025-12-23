import { z } from "zod";
import { defineTool } from "../internal/tool-helpers/define";
import { apiServiceFromContext } from "../internal/tool-helpers/api";
import type { ServerContext } from "../types";

export const createMonitor = defineTool({
  name: "create_monitor",
  skills: ["project-management"], // Using project-management or similar skill
  requiredScopes: ["org:write"],
  description: [
    "Create a new uptime monitor in GlitchTip.",
    "Use this tool to start monitoring a website or API endpoint.",
  ].join("\n"),
  inputSchema: {
    organizationSlug: z.string().describe("The organization's slug."),
    name: z
      .string()
      .describe("The name of the monitor (e.g., 'Homepage', 'API Health')."),
    url: z.string().url().describe("The URL to monitor."),
    monitorType: z
      .enum(["http", "ping", "ssl"]) // Adjust based on strict GlitchTip types if known, generic for now
      .default("http")
      .describe("The type of monitor (default: http)."),
    interval: z
      .string()
      .default("60")
      .describe(
        "Check interval in minutes (or seconds format depending on API, usually '60S' or '1m'). Passing a string like '60' often works as seconds or minutes.",
      ),
    project: z
      .union([z.string(), z.number()])
      .optional()
      .describe("Optional project ID or slug to associate with."),
  },
  annotations: {
    readOnlyHint: false,
    destructiveHint: false,
    openWorldHint: true,
  },
  async handler(params, context: ServerContext) {
    const apiService = apiServiceFromContext(context);
    const monitor = await apiService.createMonitor(params.organizationSlug, {
      name: params.name,
      url: params.url,
      monitorType: params.monitorType,
      interval: params.interval,
      project: params.project,
    });

    return [
      `# Monitor Created!`,
      `Successfully created uptime monitor: **${monitor.name}**`,
      `- URL: ${monitor.url}`,
      `- Type: ${monitor.monitor_type}`,
      `- Interval: ${monitor.interval}`,
      `- ID: ${monitor.id}`,
    ].join("\n");
  },
});
