import { existsSync } from "fs";
import http from "http";
import { Project } from "../../../shared/models";
import { handleBadRequest } from "./handleBadRequest";
import { consumeBody } from "./helpers/consumeBody";
import { saveToFile } from "./helpers/saveToFile";
import { validateProject } from "./helpers/validators";

export async function handleUpdateProject(
  req: http.IncomingMessage,
  res: http.ServerResponse
): Promise<void> {
  // Read the contents of the body as a string
  const body = await consumeBody(req);
  if (body !== "") {
    try {
      // Assume the body is json
      const object: unknown = JSON.parse(body);
      // Validate that the body is a Project
      if (validateProject(object)) {
        // Overwrite the contents of the project file with the new contents
        const result = await updateProject(object);
        if (result === "fail") {
          handleBadRequest(res, "failed to update project");
        } else {
          res.writeHead(200);
          res.end();
        }
      } else {
        console.log(object);
        handleBadRequest(res, "body has wrong format");
      }
    } catch (error) {
      handleBadRequest(res, "not a valid json");
    }
  }
}

async function updateProject(project: Project): Promise<"success" | "fail"> {
  const path = `/projects/${project.id}.json`;
  const fullPath = `./data${path}`;
  // Check that the project file exists
  if (existsSync(fullPath)) {
    // Overwrite the project the file with the new contents
    await saveToFile<Project>(path, project);
    return "success";
  } else {
    return "fail";
  }
}
