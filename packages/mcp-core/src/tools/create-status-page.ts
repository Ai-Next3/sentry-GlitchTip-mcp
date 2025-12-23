import { z } from "zod";
import { apiServiceFromContext } from "../internal/tool-helpers/api.js";
import { defineTool } from "../internal/tool-helpers/define.js";

export const createStatusPage = defineTool({
  name: "create_status_page",
  description: [
    "Create a new status page in GlitchTip.",
    "Status pages allow you to publicly communicate operational status.",
  ].join("\n"),
  inputSchema: {
    organizationSlug: z.string().describe("The organization's slug."),
    name: z.string().describe("The name of the status page."),
    slug: z
      .string()
      .describe("The URL slug for the status page (must be unique)."),
    is_public: z
      .boolean()
      .default(true)
      .describe("Whether the page is public (default: true)."),
    domain: z
      .string()
      .optional()
      .describe("Custom domain for the status page."),
  },

  requiredScopes: ["org:write"],
  skills: ["project-management"],
  annotations: {
    destructiveHint: true,
  },

  handler: async (args, context) => {
    const apiService = apiServiceFromContext(context);

    // We explicitly pass arguments to the API method to ensure correct types
    const page = await apiService.createStatusPage(args.organizationSlug, {
      name: args.name,
      slug: args.slug,
      is_public: args.is_public,
      domain: args.domain,
    });

    return [
      `# Status Page Created!`,
      `Successfully created status page: **${page.name}**`,
      `- Slug: ${page.slug}`,
      `- Public: ${page.is_public}`,
      `- Domain: ${page.domain || "N/A"}`,
      `- ID: ${page.id}`,
    ].join("\n");
  },
});
