import http from "http";
import { v4 as uuidv4 } from "uuid";
import { Project, User } from "../../../shared/models";
import { handleBadRequest } from "./handleBadRequest";
import { consumeBody } from "./helpers/consumeBody";
import { createDirIfNotExist } from "./helpers/createDirIfNotExist";
import { readFromFile } from "./helpers/readFromFile";
import { saveToFile } from "./helpers/saveToFile";
import { validateNewProject, validateUser } from "./helpers/validators";

// Example:
// POST /projects
// Response:
// {
//   "projectId": "123e4567-e89b-12d3-a456-426614174000"
// }
export async function handleNewProject(
  req: http.IncomingMessage,
  res: http.ServerResponse
) {
  const body = await consumeBody(req);
  // Validate the request
  if (body !== "") {
    try {
      const object: unknown = JSON.parse(body);

      if (validateNewProject(object)) {
        // Create the project
        const project: Project = await createProject(object.userId);
        // Respond with the created project
        res.writeHead(200);
        res.end(JSON.stringify(project));
      } else {
        handleBadRequest(res, "body has wrong format");
      }
    } catch (error) {
      handleBadRequest(res, "not valid json");
    }
  } else {
    handleBadRequest(res, "body is empty");
  }
}

export async function createProject(userId: string): Promise<Project> {
  // Create an id for the project
  const id = uuidv4();

  // Ensure projects directory is created
  await createDirIfNotExist("./data");
  await createDirIfNotExist("./data/projects");

  const project: Project = {
    id,
    trackPair: {
      melodyTrack: { type: "melody", events: [] },
      chordTrack: { type: "chords", events: [] },
    },
  };

  // Create a file for the project
  await saveToFile<Project>(`/projects/${id}.json`, project);

  // Add to user file
  await addProjectToUserFile(userId, id);

  return project;
}

async function addProjectToUserFile(userId: string, projectId: string) {
  const userFileName = `/users/${userId}.json`;

  // Make sure the "/data/users" directory is present
  await createDirIfNotExist("./data");
  await createDirIfNotExist("./data/users/");

  // Read the current contents of the user file
  const userFile: User = (await readFromFile<User>(
    userFileName,
    validateUser
  )) ?? {
    id: userId,
    projects: [],
  };

  // Add the new project to that object
  userFile.projects.push(projectId);

  // Save the new version of the user file
  await saveToFile<User>(userFileName, userFile);
}
