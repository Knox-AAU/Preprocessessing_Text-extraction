import { AttackRelease, Project } from "../../../shared/models";
import { getTracks } from "./getTracks";

export function getAllProjectEvents(project: Project): AttackRelease[] {
  return getTracks(project).flatMap((t) => t.events);
}
