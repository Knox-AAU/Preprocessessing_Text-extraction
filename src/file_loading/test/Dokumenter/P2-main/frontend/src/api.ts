import { AttackRelease, Project, Track } from "../../shared/models";
import { baseApiUrl } from "./constants";
import { debounce } from "./helpers/debounce";

export async function saveProject(project: Project): Promise<void> {
  await fetch(`${baseApiUrl}/projects`, {
    body: JSON.stringify(project),
    method: "PUT",
  });
}

export const saveProjectDebounced = debounce(saveProject, 2000);

export async function getProject(projectId: string): Promise<Project | null> {
  const response = await fetch(`${baseApiUrl}/projects?id=${projectId}`);
  if (response.status === 200) {
    return await response.json();
  } else {
    return null;
  }
}

export async function newProject(userId: string): Promise<Project | null> {
  const response = await fetch(`${baseApiUrl}/projects`, {
    body: JSON.stringify({ userId }),
    method: "POST",
  });
  if (response.status === 200) {
    return await response.json();
  } else {
    return null;
  }
}

// Add an event to the selected track and schedule the project to be saved
export function addEventAndSave(
  project: Project,
  selectedTrack: Track,
  event: AttackRelease
) {
  selectedTrack.events.push(event);
  saveProjectDebounced(project);
}

// Removes the events from the project and schedules a save to the backend
export function removeEventAndSave(
  project: Project,
  track: Track,
  deleteIndex: number
) {
  track.events.splice(deleteIndex, 1);
  saveProjectDebounced(project);
}
