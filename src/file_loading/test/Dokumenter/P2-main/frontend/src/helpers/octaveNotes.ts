import { OctaveNote } from "../../../shared/models";
import { notes, octaves } from "../constants";

export function octaveNoteString(octaveNote: OctaveNote): string {
  return octaveNote.note + octaveNote.octave;
}

export function getOctaveRowIndex(octaveNote: OctaveNote): number {
  return (
    notes.indexOf(octaveNote.note) +
    octaves.indexOf(octaveNote.octave) * notes.length
  );
}

export function octaveNoteEquals(a: OctaveNote, b: OctaveNote): boolean {
  return octaveNoteString(a) === octaveNoteString(b);
}
