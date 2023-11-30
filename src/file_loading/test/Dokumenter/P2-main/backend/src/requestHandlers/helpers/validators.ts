import { validate as uuidValidate } from "uuid";
import {
  AttackRelease,
  NewProject,
  OctaveNote,
  Project,
  Track,
  TrackPair,
  User,
} from "../../../../shared/models";

// The functions in this file checks if objects are of a given type and contains
// the correct values

export function validateNewProject(object: unknown): object is NewProject {
  return (
    typeof object === "object" &&
    object !== null &&
    typeof (object as NewProject).userId === "string" &&
    uuidValidate((object as NewProject).userId)
  );
}

export function validateProject(object: unknown): object is Project {
  return (
    typeof (object as Project).id === "string" &&
    uuidValidate((object as Project).id) &&
    validateTrackPair((object as Project).trackPair)
  );
}

export function validateTrackPair(object: unknown): object is TrackPair {
  return (
    typeof object === "object" &&
    object !== null &&
    validateTrack((object as TrackPair).chordTrack) &&
    validateTrack((object as TrackPair).melodyTrack)
  );
}

export function validateTrack(object: Track): object is Track {
  return (
    typeof object === "object" &&
    object !== null &&
    typeof (object as Track).type === "string" &&
    Array.isArray((object as Track).events) &&
    (object as Track).events
      .map((e) => validateAttackRelease(e))
      .reduce((a, b) => a && b, true)
  );
}

export function validateAttackRelease(
  object: unknown
): object is AttackRelease {
  return (
    typeof object === "object" &&
    object !== null &&
    typeof (object as AttackRelease).start === "number" &&
    typeof (object as AttackRelease).end === "number" &&
    validateOctaveNote((object as AttackRelease).octaveNote)
  );
}

function validateOctaveNote(object: unknown): object is OctaveNote {
  return (
    typeof object === "object" &&
    object !== null &&
    typeof (object as OctaveNote).note === "string" &&
    typeof (object as OctaveNote).octave === "number"
  );
}

export function validateUser(object: unknown): object is User {
  return (
    typeof object === "object" &&
    object !== null &&
    typeof (object as User).id === "string" &&
    uuidValidate((object as User).id) &&
    Array.isArray((object as User).projects) &&
    (object as User).projects
      .map((p) => typeof p === "string")
      .reduce((a, b) => a && b, true)
  );
}
