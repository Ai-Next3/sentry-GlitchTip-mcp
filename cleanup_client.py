import sys

path = "packages/mcp-core/src/api-client/client.ts"
print(f"Reading {path}")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Define the CLEAN block
clean_block = """  async listEventAttachments(
    {
      organizationSlug,
      projectSlug,
      eventId,
    }: {
      organizationSlug: string;
      projectSlug: string;
      eventId: string;
    },
    opts?: RequestOptions,
  ): Promise<EventAttachmentList> {
    const body = await this.requestJSON(
      `/api/0/projects/${organizationSlug}/${projectSlug}/events/${eventId}/attachments/`,
      undefined,
      opts,
    );
    return EventAttachmentListSchema.parse(body);
  }

  async getEventAttachment(
    {
      organizationSlug,
      projectSlug,
      eventId,
      attachmentId,
    }: {
      organizationSlug: string;
      projectSlug: string;
      eventId: string;
      attachmentId: string;
    },
    opts?: RequestOptions,
  ): Promise<{
    attachment: EventAttachment;
    downloadUrl: string;
    filename: string;
    blob: Blob;
  }> {
    // Get the attachment metadata first
    const attachmentsData = await this.requestJSON(
      `/api/0/projects/${organizationSlug}/${projectSlug}/events/${eventId}/attachments/`,
      undefined,
      opts,
    );

    const attachments = EventAttachmentListSchema.parse(attachmentsData);
    const attachment = attachments.find((att) => att.id === attachmentId);

    if (!attachment) {
      throw new ApiNotFoundError(
        `Attachment with ID ${attachmentId} not found for event ${eventId}`,
      );
    }

    // Download the actual file content
    const downloadUrl =
      `/api/0/projects/${organizationSlug}/${projectSlug}/events/${eventId}/attachments/${attachmentId}/?download=1`;

    const downloadResponse = await this.request(
      downloadUrl,
      {
        method: "GET",
        headers: {
          Accept: "application/octet-stream",
        },
      },
      opts,
    );

    return {
      attachment,
      downloadUrl: downloadResponse.url,
      filename: attachment.name,
      blob: await downloadResponse.blob(),
    };
  }
"""

start_marker = "async listEventAttachments("
end_marker = "async updateIssue("

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print(f"FATAL: Could not find markers. Start: {start_idx}, End: {end_idx}")
    sys.exit(1)

print(f"Replacing chunk from {start_idx} to {end_idx}")

# Preserve indentation of the start marker?
# The replacement text already has 2-space indentation.
# We just replace directly.

new_content = content[:start_idx] + clean_block + "\n  " + content[end_idx:]

with open(path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Massive cleanup complete.")
