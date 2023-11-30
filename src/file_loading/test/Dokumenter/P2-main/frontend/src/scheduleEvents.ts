import { Sampler, Time, Transport } from "tone";
import { AttackRelease, Project } from "../../shared/models";
import { defaultVelocity } from "./constants";
import { getAllProjectEvents } from "./helpers/getAllProjectEvents";
import { octaveNoteString } from "./helpers/octaveNotes";

// Schedules the events of a project to be played
export function scheduleEvents(sampler: Sampler, project: Project) {
  // Stop any scheduled events from being played
  Transport.cancel();
  // Schedule all events to be played
  getAllProjectEvents(project).forEach((e) => {
    scheduleEvent(sampler, e);
  });
}

function scheduleEvent(sampler: Sampler, event: AttackRelease) {
  sampler.triggerAttack(
    octaveNoteString(event.octaveNote),
    Time("16n").toSeconds() * event.start,
    defaultVelocity
  );
  sampler.triggerRelease(
    [octaveNoteString(event.octaveNote)],
    Time("16n").toSeconds() * event.end - 0.005
  );
}
