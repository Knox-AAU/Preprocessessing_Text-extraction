import { AttackRelease, OctaveNote, Project, Track } from "../../shared/models";
import { notes } from "./constants";
import { getAllProjectEvents } from "./helpers/getAllProjectEvents";
import {
  getOctaveRowIndex,
  octaveNoteEquals,
  octaveNoteString,
} from "./helpers/octaveNotes";
import { notesDissonance } from "./ratios";

export function determineSuggestionsForTime(
  time: number,
  project: Project,
  selectedTrack: Track,
  octaveNote: OctaveNote
) {
  if (selectedTrack.type === "melody") {
    return determineMelodySuggestionsForTime(time, project, selectedTrack);
  } else {
    return new Set(
      determineChordSuggestionForTime(
        time,
        project,
        selectedTrack,
        octaveNote
      ).map(octaveNoteString)
    );
  }
}

export function determineMelodySuggestionsForTime(
  time: number,
  project: Project,
  selectedTrack: Track
): Set<string> {
  // All the events in the considered range for the track
  const eventsInRange = getEventsInConsideredRange(time, selectedTrack);

  // Don't suggest melody if there is already something at that time
  if (eventsInRange.find((e) => e.start === time)) {
    return new Set();
  }

  // Returns all the scales that have usedNotes as a subset
  return getPossibleScales(time, project).reduce(
    (a, b) => new Set([...a, ...b]),
    new Set()
  );
}

export function getPossibleScales(
  time: number,
  project: Project
): Set<string>[] {
  const scales = generateMajorScales();

  // All the events in the considered range for all the tracks
  const eventsInRange = getAllProjectEvents(project).filter((e) =>
    isEventInConsideredRange(time, e)
  );

  // All the notes that are within the range
  const usedNotes = new Set(eventsInRange.map((e) => e.octaveNote.note));

  // Returns all the scales that have usedNotes as a subset
  return scales.filter((scale) =>
    isSubset({ lhs: usedNotes, rhs: intersection(scale, usedNotes) })
  );
}

function getEventsInConsideredRange(time: number, track: Track) {
  // All the events in the considered range for the track
  return track.events.filter((e) => isEventInConsideredRange(time, e));
}

function isEventInConsideredRange(time: number, event: AttackRelease): boolean {
  const measureAtTime = Math.floor(time / 16);
  // Sixteenths included before the measure in the considered range
  const preMeasure = 4;

  // Defines the range of start time that is being considered
  const start = measureAtTime * 16 - preMeasure;
  const end = measureAtTime * 16 + 16;

  return event.start >= start && event.start < end;
}

export function determineChordSuggestionForTime(
  time: number,
  project: Project,
  selectedTrack: Track,
  startOctaveNote: OctaveNote
): OctaveNote[] {
  const possibleScales = getPossibleScales(time, project);
  const scalesWithNote = possibleScales.filter((s) =>
    s.has(startOctaveNote.note)
  );

  const alreadyHasEventsAtTime = selectedTrack.events.find(
    (e) => e.start === time
  );

  const eventsAtTime = getAllProjectEvents(project).filter(
    (e) => time >= e.start && time < e.end
  );

  const scoredChords: [number, OctaveNote[]][] = scalesWithNote
    .map(chordFromScale(startOctaveNote, eventsAtTime))
    // One chords that include the start octave note
    .filter((chord) =>
      chord.some((chordOctaveNote) =>
        octaveNoteEquals(chordOctaveNote, startOctaveNote)
      )
    )
    .map((chord) => [
      notesDissonance([...chord, ...eventsAtTime.map((e) => e.octaveNote)]),
      chord,
    ]);

  if (scoredChords.length === 0 || alreadyHasEventsAtTime) return [];

  // Sort chords by dissonance (least to most)
  scoredChords.sort(
    ([aDissonance], [bDissonance]) => aDissonance - bDissonance
  );

  // Return the chord with the least dissonance
  return scoredChords[0][1];
}

function chordFromScale(
  octaveNote: OctaveNote,
  eventsAtTime: AttackRelease[]
): (
  value: Set<string>,
  index: number,
  array: Set<string>[]
) => { note: string; octave: number }[] {
  return (scale) => {
    const scaleInOrder = notes.filter((n) => scale.has(n)).reverse();

    const startIndex = scaleInOrder.indexOf(octaveNote.note);

    const offsets = [0, 2, 4];

    const chord = offsets
      .map(
        (offset) => scaleInOrder[(startIndex + offset) % scaleInOrder.length]
      )
      .map((chordNote) => ({
        note: chordNote,
        octave:
          // One octave higher than the base octave if the current chord note is
          // before the start of the scale (wrapped around)
          startIndex <= scaleInOrder.indexOf(chordNote)
            ? octaveNote.octave
            : octaveNote.octave + 1,
      }))
      // Invert chord notes based on all the other events at that time
      .map((chordOctaveNote) => {
        while (
          // Any event where the chord note is above
          eventsAtTime.some(
            (e) =>
              getOctaveRowIndex(e.octaveNote) >
              getOctaveRowIndex(chordOctaveNote)
          ) ||
          getLowestNoteDistance(chordOctaveNote, eventsAtTime) < 3
        ) {
          // Move one octave down
          chordOctaveNote.octave--;
        }
        return chordOctaveNote;
      });

    return chord;
  };
}

function getLowestNoteDistance(
  octaveNote: OctaveNote,
  eventsAtTime: AttackRelease[]
) {
  return Math.min(
    ...eventsAtTime.map((e) => octaveNoteDistance(octaveNote, e.octaveNote))
  );
}

export function octaveNoteDistance(a: OctaveNote, b: OctaveNote): number {
  return Math.abs(getOctaveRowIndex(a) - getOctaveRowIndex(b));
}

// Generates all the possible major scales
function generateMajorScales(): Set<string>[] {
  // All notes in the major scale
  const offsets = [0, 2, 4, 5, 7, 9, 11];
  // Creates a set of arrays containing every major scale from every note
  return notes.map(
    (_, i) =>
      new Set(offsets.map((offset) => notes[(offset + i) % notes.length]))
  );
}

function intersection<T>(s1: Set<T>, s2: Set<T>): Set<T> {
  return new Set([...s1].filter((value) => s2.has(value)));
}

function isSubset<T>({ lhs, rhs }: { lhs: Set<T>; rhs: Set<T> }): boolean {
  return [...lhs].every((value) => rhs.has(value));
}
