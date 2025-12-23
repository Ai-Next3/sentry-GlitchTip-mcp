import { SentryApiService } from "./packages/mcp-core/src/api-client/client";

const SENTRY_HOST = "glitchtip.your-domain.com";
// Token redacted for security
const SENTRY_ACCESS_TOKEN =
  process.env.SENTRY_ACCESS_TOKEN || "your-token-here";

async function main() {
  console.log("🚀 Starting GlitchTip Verification...");

  const api = new SentryApiService({
    accessToken: SENTRY_ACCESS_TOKEN,
    host: SENTRY_HOST,
  });

  try {
    // 0. User Info
    console.log("👤 Verifying User Info...");
    const user = await api.getAuthenticatedUser();
    console.log(`✅ Logged in as: ${user.email} (${user.id})`);
    // 1. List Organizations
    console.log("\n📋 Listing Organizations...");
    const orgs = await api.listOrganizations();
    console.log(`✅ Found ${orgs.length} organizations.`);
    if (orgs.length === 0) {
      console.error("No organizations found. Cannot proceed.");
      return;
    }
    const org = orgs[0];
    console.log(`Using organization: ${org.slug}`);

    // 1a. List Teams
    console.log(`\n👥 Listing Teams for ${org.slug}...`);
    try {
      const teams = await api.listTeams(org.slug);
      console.log(`✅ Found ${teams.length} teams.`);
      if (teams.length > 0) console.log(`   - First team: ${teams[0].slug}`);
    } catch (e) {
      console.error("❌ Failed to list teams:", e);
    }

    // 1b. List Releases
    console.log(`\n📦 Listing Releases for ${org.slug}...`);
    try {
      const releases = await api.listReleases({ organizationSlug: org.slug });
      console.log(`✅ Found ${releases.length} releases.`);
      if (releases.length > 0)
        console.log(`   - Latest release: ${releases[0].version}`);
    } catch (e) {
      // Releases might be empty or fail if not configured, optional check
      console.log(
        "ℹ️  Releases check (optional):",
        e instanceof Error ? e.message : String(e),
      );
    }

    // 2. List Monitors
    console.log(`\n📡 Listing Monitors for ${org.slug}...`);
    try {
      const monitors = await api.listMonitors(org.slug);
      console.log(`✅ Success! Found ${monitors.length} monitors.`);
      for (const m of monitors) {
        console.log(
          `   - ${m.name} (${m.monitor_type}): ${m.is_up ? "UP" : "DOWN"}`,
        );
      }
    } catch (e) {
      console.error("❌ Failed to list monitors:", e);
    }

    // 3. List Status Pages
    console.log(`\nqm Listing Status Pages for ${org.slug}...`);
    try {
      const pages = await api.listStatusPages(org.slug);
      console.log(`✅ Success! Found ${pages.length} status pages.`);
      for (const p of pages) {
        console.log(`   - ${p.name}: ${p.slug}`);
      }
    } catch (e) {
      console.error("❌ Failed to list status pages:", e);
    }

    // 4. Alerts
    console.log(`\n🚨 Verification: Alerts for ${org.slug}...`);
    try {
      const projects = await api.listProjects(org.slug);
      if (projects.length === 0) {
        console.log("No projects found, skipping alerts verification.");
      } else {
        const project = projects[0];
        console.log(`Using project: ${project.slug}`);

        console.log("Listing alerts...");
        const alerts = await api.listAlerts(org.slug, project.slug);
        console.log(`Found ${alerts.length} alerts.`);

        const testAlertName = `Test Alert ${Date.now()}`;
        console.log(`Creating alert: ${testAlertName}`);
        const newAlert = await api.createAlert(org.slug, project.slug, {
          name: testAlertName,
          frequency: 60,
          actionMatch: "all",
        });
        console.log(`✅ Created alert: ${newAlert.name} (${newAlert.id})`);
      }
    } catch (e) {
      console.error("❌ Failed to verify alerts:", e);
    }

    // 5. Issues & Events (Core)
    console.log(`\n🔍 Verifying Issues & Events for ${org.slug}...`);
    try {
      const issues = await api.listIssues({
        organizationSlug: org.slug,
        query: "is:unresolved",
        limit: 5,
      });
      console.log(`✅ Found ${issues.length} unresolved issues.`);

      if (issues.length > 0) {
        const firstIssue = issues[0];
        console.log(
          `   - First issue: ${firstIssue.title} (${firstIssue.shortId})`,
        );

        // 6. Issue Details
        console.log(`\n📄 Verifying Issue Details for ${firstIssue.id}...`);
        try {
          const issueDetails = await api.getIssue({
            organizationSlug: org.slug,
            issueId: String(firstIssue.id), // Note: client.ts getIssue expects string issueId
          });
          console.log(`✅ Fetched details for: ${issueDetails.title}`);
          console.log(`   - Permlink: ${issueDetails.permalink}`);
        } catch (e) {
          console.error("❌ Failed to get issue details:", e);
        }

        // Search events for this issue
        console.log(`\n🔎 Searching events for issue ${firstIssue.id}...`);

        // Use searchErrors for event search
        const errors = await api.searchErrors({
          organizationSlug: org.slug,
          query: `issue:${issues[0].shortId}`,
          sortBy: "last_seen",
        });
        console.log(`✅ Found ${errors.length} errors related to issue.`);
      }

      // Search global events
      console.log("   - Searching global events (last 24h)...");
      const recentErrors = await api.searchErrors({
        organizationSlug: org.slug,
        query: "",
        sortBy: "last_seen",
      });
      console.log(`✅ Found ${recentErrors.length} recent global errors.`);
    } catch (e) {
      console.error("❌ Failed to verify issues:", e);
    }
  } catch (error) {
    console.error("❌ Fatal error:", error);
  }
}

main();
