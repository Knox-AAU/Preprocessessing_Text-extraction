import { Project } from "../../../shared/models";

export function getTracks(project: Project) {
  return [project.trackPair.melodyTrack, project.trackPair.chordTrack];
}
