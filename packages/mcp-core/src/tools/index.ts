import whoami from "./whoami";
import findOrganizations from "./find-organizations";
import findTeams from "./find-teams";
import findProjects from "./find-projects";
import findReleases from "./find-releases";
import getIssueDetails from "./get-issue-details";
import getTraceDetails from "./get-trace-details";
import getEventAttachment from "./get-event-attachment";
import updateIssue from "./update-issue";
import searchEvents from "./search-events";
import createTeam from "./create-team";
import createProject from "./create-project";
import updateProject from "./update-project";
import createDsn from "./create-dsn";
import findDsns from "./find-dsns";
import analyzeIssueWithSeer from "./analyze-issue-with-seer";
import { searchDocs } from "./search-docs.js";
import getDoc from "./get-doc";
import searchIssues from "./search-issues";
import searchIssueEvents from "./search-issue-events";
import useSentry from "./use-sentry";

import { listMonitors } from "./list-monitors.js";
import { createMonitor } from "./create-monitor.js";

import { listStatusPages } from "./list-status-pages.js";
import { createStatusPage } from "./create-status-page.js";

import { listAlerts } from "./list-alerts.js";
import { createAlert } from "./create-alert.js";

// Default export: object mapping tool names to tools
export default {
  whoami,
  find_organizations: findOrganizations,
  find_teams: findTeams,
  find_projects: findProjects,
  find_releases: findReleases,
  get_issue_details: getIssueDetails,
  get_trace_details: getTraceDetails,
  get_event_attachment: getEventAttachment,
  update_issue: updateIssue,
  search_events: searchEvents,
  create_team: createTeam,
  create_project: createProject,
  update_project: updateProject,
  create_dsn: createDsn,
  find_dsns: findDsns,
  analyze_issue_with_seer: analyzeIssueWithSeer,
  search_docs: searchDocs,
  get_doc: getDoc,
  search_issues: searchIssues,
  search_issue_events: searchIssueEvents,
  use_sentry: useSentry,
  list_monitors: listMonitors,
  create_monitor: createMonitor,
  list_status_pages: listStatusPages,
  create_status_page: createStatusPage,
  list_alerts: listAlerts,
  create_alert: createAlert,
} as const;

// Type export
export type ToolName = keyof typeof import("./index").default;
