const organizationSlug = "org";
const issueId = "123";
const params = new URLSearchParams();
const apiUrl = `/api/0/organizations/${organizationSlug}/issues/${issueId}/events/?${params.toString()}`;
console.log(apiUrl);
