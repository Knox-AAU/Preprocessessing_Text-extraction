import http from "http";
import { Project } from "../../../shared/models";
import { handleBadRequest } from "./handleBadRequest";
import { getUrlFromRequest } from "./helpers/getUrlFromRequest";
import { readFromFile } from "./helpers/readFromFile";
import { validateProject } from "./helpers/validators";

// Example:
// GET /projects?id=456e4567-e89b-12d3-a456-426614174000
// Response:
// Project
export async function handleFindProject(
  req: http.IncomingMessage,
  res: http.ServerResponse
): Promise<void> {
  // Get the project id from the search params
  const url = getUrlFromRequest(req)!;
  const id = url.searchParams.get("id");

  if (id !== null) {
    // Read project from file
    const project: Project | null = await readFromFile(
      `/projects/${id}.json`,
      validateProject
    );
    if (project !== null) {
      // Send it in the response
      res.writeHead(200);
      res.end(JSON.stringify(project));
    } else {
      await handleBadRequest(res, "project does not exist");
    }
  } else {
    await handleBadRequest(res, "no id provided");
  }
}
