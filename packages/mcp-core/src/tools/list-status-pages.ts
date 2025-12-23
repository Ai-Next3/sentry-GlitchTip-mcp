import { z } from "zod";
import { apiServiceFromContext } from "../internal/tool-helpers/api.js";
import { defineTool } from "../internal/tool-helpers/define.js";

export const listStatusPages = defineTool({
  name: "list_status_pages",
  description: [
    "List all status pages for an organization in GlitchTip.",
    "Use this tool to see what public status pages are configured.",
  ].join("\n"),
  inputSchema: {
    organizationSlug: z.string().describe("The organization's slug."),
  },

  requiredScopes: ["org:read"],
  skills: ["project-management", "monitoring"],
  annotations: {
    readOnlyHint: true,
  },

  handler: async (args, context) => {
    const apiService = apiServiceFromContext(context);
    const pages = await apiService.listStatusPages(args.organizationSlug);

    if (pages.length === 0) {
      return "No status pages found for this organization.";
    }

    let output = `# Status Pages for ${args.organizationSlug}\n\n`;

    for (const page of pages) {
      const status = page.is_public ? "🌍 Public" : "🔒 Private";
      output += `- **${page.name}** (${status})\n`;
      output += `  - Slug: ${page.slug}\n`;
      output += `  - Domain: ${page.domain || "None"}\n`;
      output += `  - ID: ${page.id}\n`;
      output += "\n";
    }

    return output;
  },
});
