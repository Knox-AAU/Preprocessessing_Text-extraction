import { assert, describe, expect, test } from "vitest";
import { Project, Track } from "../../shared/models";
import { notes } from "../src/constants";
import { octaveNoteString } from "../src/helpers/octaveNotes";
import {
  determineChordSuggestionForTime,
  getPossibleScales,
  octaveNoteDistance,
} from "../src/suggestions";

const cMajor = new Set(["F", "G", "A", "C", "D", "E", "B"]);
const gMajor = new Set(["F#", "G", "A", "C", "D", "E", "B"]);

describe("getPossibleScales", () => {
  test("C major", () => {
    const track: Track = {
      events: [
        { octaveNote: { note: "C", octave: 5 }, end: 1, start: 0 },
        { octaveNote: { note: "D", octave: 5 }, end: 2, start: 1 },
        { octaveNote: { note: "E", octave: 5 }, end: 3, start: 2 },
        { octaveNote: { note: "F", octave: 5 }, end: 4, start: 3 },
        { octaveNote: { note: "G", octave: 5 }, end: 5, start: 4 },
        { octaveNote: { note: "A", octave: 5 }, end: 6, start: 5 },
        { octaveNote: { note: "B", octave: 5 }, end: 7, start: 6 },
      ],
      type: "melody",
    };
    const project: Project = {
      id: "",
      trackPair: { melodyTrack: track, chordTrack: emptyTrack("chords") },
    };

    const possibleScales = getPossibleScales(7, project);
    expect(possibleScales).lengthOf(1);
    assertSuggestionEqual(possibleScales[0], cMajor);
  });

  test("no possible", () => {
    const track: Track = {
      events: [
        { octaveNote: { note: "A", octave: 5 }, end: 1, start: 0 },
        { octaveNote: { note: "B", octave: 5 }, end: 2, start: 1 },
        { octaveNote: { note: "C", octave: 5 }, end: 3, start: 2 },
        { octaveNote: { note: "C#", octave: 5 }, end: 4, start: 3 },
      ],
      type: "melody",
    };
    const project: Project = {
      id: "",
      trackPair: { melodyTrack: track, chordTrack: emptyTrack("chords") },
    };

    const possibleScales = getPossibleScales(7, project);
    expect(possibleScales).lengthOf(0);
  });

  test("C major and G major", () => {
    const track: Track = {
      events: [
        { octaveNote: { note: "C", octave: 5 }, end: 1, start: 0 },
        { octaveNote: { note: "D", octave: 5 }, end: 2, start: 1 },
        { octaveNote: { note: "E", octave: 5 }, end: 3, start: 2 },
        { octaveNote: { note: "G", octave: 5 }, end: 5, start: 4 },
        { octaveNote: { note: "A", octave: 5 }, end: 6, start: 5 },
        { octaveNote: { note: "B", octave: 5 }, end: 7, start: 6 },
      ],
      type: "melody",
    };
    const project: Project = {
      id: "",
      trackPair: { melodyTrack: track, chordTrack: emptyTrack("chords") },
    };

    const possibleScales = getPossibleScales(7, project);
    expect(possibleScales).lengthOf(2);

    const possibleCMajor = possibleScales.find((s) => s.has("F"));
    const possibleGMajor = possibleScales.find((s) => s.has("F#"));

    expect(possibleCMajor).not.toBeUndefined();
    assertSuggestionEqual(possibleCMajor, cMajor);

    expect(possibleGMajor).not.toBeUndefined();
    assertSuggestionEqual(possibleGMajor, gMajor);
  });

  test("no events", () => {
    const track: Track = {
      events: [],
      type: "melody",
    };
    const project: Project = {
      id: "",
      trackPair: { melodyTrack: track, chordTrack: emptyTrack("chords") },
    };

    const possibleScales = getPossibleScales(0, project);
    expect(possibleScales).lengthOf(notes.length);
  });

  test("ignore out of bounds measure", () => {
    const track: Track = {
      events: [
        { octaveNote: { note: "C", octave: 5 }, end: 1, start: 0 },
        { octaveNote: { note: "D", octave: 5 }, end: 2, start: 1 },
        { octaveNote: { note: "E", octave: 5 }, end: 3, start: 2 },
        { octaveNote: { note: "F", octave: 5 }, end: 4, start: 3 },
        { octaveNote: { note: "G", octave: 5 }, end: 5, start: 4 },
        { octaveNote: { note: "A", octave: 5 }, end: 6, start: 5 },
        { octaveNote: { note: "B", octave: 5 }, end: 7, start: 6 },
        { octaveNote: { note: "F#", octave: 5 }, end: 17, start: 16 },
      ],
      type: "melody",
    };
    const project: Project = {
      id: "",
      trackPair: { melodyTrack: track, chordTrack: emptyTrack("chords") },
    };
    const possibleScales = getPossibleScales(14, project);

    expect(possibleScales).lengthOf(1);
    assertSuggestionEqual(possibleScales[0], cMajor);
  });
});

describe("octaveNoteDistance", () => {
  test("Within same octave", () => {
    expect(
      octaveNoteDistance({ note: "C", octave: 1 }, { note: "C", octave: 1 })
    ).toEqual(0);
    expect(
      octaveNoteDistance({ note: "C", octave: 1 }, { note: "E", octave: 1 })
    ).toEqual(4);
    expect(
      octaveNoteDistance({ note: "E", octave: 1 }, { note: "C", octave: 1 })
    ).toEqual(4);
    expect(
      octaveNoteDistance({ note: "A#", octave: 1 }, { note: "C", octave: 1 })
    ).toEqual(10);
  });

  test("Across octaves", () => {
    expect(
      octaveNoteDistance({ note: "C", octave: 1 }, { note: "C", octave: 2 })
    ).toEqual(12);
    expect(
      octaveNoteDistance({ note: "C", octave: 2 }, { note: "E", octave: 1 })
    ).toEqual(8);
    expect(
      octaveNoteDistance({ note: "E", octave: 2 }, { note: "C", octave: 1 })
    ).toEqual(16);
    expect(
      octaveNoteDistance({ note: "A#", octave: 1 }, { note: "C", octave: 2 })
    ).toEqual(2);
  });
});

describe("Chord suggestions", () => {
  const cMajorMelodyProject: Project = {
    id: "",
    trackPair: {
      melodyTrack: {
        type: "melody",
        events: [
          { octaveNote: { note: "B", octave: 5 }, end: 1, start: 0 },
          { octaveNote: { note: "A", octave: 5 }, end: 2, start: 1 },
          { octaveNote: { note: "G", octave: 5 }, end: 3, start: 2 },
          { octaveNote: { note: "F", octave: 5 }, end: 4, start: 3 },
          { octaveNote: { note: "E", octave: 5 }, end: 5, start: 4 },
          { octaveNote: { note: "D", octave: 5 }, end: 6, start: 5 },
          { octaveNote: { note: "C", octave: 5 }, end: 7, start: 6 },
        ],
      },
      chordTrack: { type: "chords", events: [] },
    },
  };

  test("On melody notes", () => {
    expect(
      determineChordSuggestionForTime(
        1,
        cMajorMelodyProject,
        cMajorMelodyProject.trackPair.chordTrack,
        { note: "A", octave: 5 }
      )
    ).lengthOf(0);

    expect(
      determineChordSuggestionForTime(
        6,
        cMajorMelodyProject,
        cMajorMelodyProject.trackPair.chordTrack,
        { note: "C", octave: 5 }
      )
    ).lengthOf(0);
  });

  test("Over melody notes", () => {
    expect(
      determineChordSuggestionForTime(
        1,
        cMajorMelodyProject,
        cMajorMelodyProject.trackPair.chordTrack,
        { note: "A#", octave: 5 }
      )
    ).lengthOf(0);

    expect(
      determineChordSuggestionForTime(
        6,
        cMajorMelodyProject,
        cMajorMelodyProject.trackPair.chordTrack,
        { note: "C#", octave: 5 }
      )
    ).lengthOf(0);
  });

  test("Space for original chord", () => {
    expect(
      determineChordSuggestionForTime(
        1,
        cMajorMelodyProject,
        cMajorMelodyProject.trackPair.chordTrack,
        { note: "A", octave: 4 }
      )
    ).lengthOf(3);

    expect(
      determineChordSuggestionForTime(
        6,
        cMajorMelodyProject,
        cMajorMelodyProject.trackPair.chordTrack,
        { note: "C", octave: 4 }
      )
    ).lengthOf(3);
  });

  test("Chord inversion", () => {
    const g5InvertedChord = new Set(
      determineChordSuggestionForTime(
        0,
        cMajorMelodyProject,
        cMajorMelodyProject.trackPair.chordTrack,
        { note: "G", octave: 5 }
      ).map(octaveNoteString)
    );
    assert(g5InvertedChord.has("G5"));
    assert(g5InvertedChord.has("D5"));
    assert(g5InvertedChord.has("B4"));

    const d5InvertedChord = new Set(
      determineChordSuggestionForTime(
        0,
        cMajorMelodyProject,
        cMajorMelodyProject.trackPair.chordTrack,
        { note: "D", octave: 5 }
      ).map(octaveNoteString)
    );
    assert(d5InvertedChord.has("D5"));
    assert(d5InvertedChord.has("F5"));
    assert(d5InvertedChord.has("A4"));
  });
});

function assertSuggestionEqual(
  suggestion: Set<string>,
  expectedSuggestion: Set<string>
) {
  suggestion.forEach((s) => {
    assert(expectedSuggestion.has(s));
  });
  expectedSuggestion.forEach((s) => {
    assert(suggestion.has(s));
  });
}

function emptyTrack(type: "melody" | "chords"): Track {
  return { events: [], type };
}
