import { assert, describe, expect, test } from "vitest";
import {
  ratioBetween,
  lcm,
  dissonanceFactor,
  notesDissonance,
} from "../src/ratios";

describe("Test ratios in intervals", () => {
  test("Find fifth ratio", () => {
    const ratio = ratioBetween(0, 7);
    assert(ratio.num === 3 && ratio.den === 2);
  });
  test("Find second note ratio", () => {
    const ratio = ratioBetween(0, 2);
    assert(ratio.num === 9 && ratio.den === 8);
  });
  test("Find tritone ratio", () => {
    const ratio = ratioBetween(0, 6);
    assert(ratio.num === 729 && ratio.den === 512);
  });
  test("Find 5th step ratio", () => {
    const ratio = ratioBetween(0, 5);
    assert(ratio.num === 4 && ratio.den === 3);
  });
  test("Find 11 steps ratio", () => {
    const ratio = ratioBetween(3, 14);
    assert(ratio.num === 243 && ratio.den === 128);
  });
  test("Find octave ratio", () => {
    const ratio = ratioBetween(1, 13);
    expect(ratio.num).equals(2);
    expect(ratio.den).equals(1);
  });
  test("Find two octaves ratio", () => {
    const ratio = ratioBetween(1, 25);
    expect(ratio.num).equals(4);
    expect(ratio.den).equals(1);
  });
  test("Find two octaves and a step ratio", () => {
    const ratio = ratioBetween(1, 25);
    expect(ratio.num).equals(4);
    expect(ratio.den).equals(1);
  });
  test("Find reverse tritone", () => {
    const ratio = ratioBetween(7, 1);
    assert(ratio.num === 729 && ratio.den === 512);
  });
  test("Find reverse tritone", () => {
    const ratio = ratioBetween(7, 1);
    assert(ratio.num === 729 && ratio.den === 512);
  });
});

describe("Test lcm", () => {
  test("lcm(2, 8)", () => {
    assert(lcm(2, 8) === 8);
  });
});

describe("Check dissonance", () => {
  test("Fifth more consonant than tritone", () => {
    expect(dissonanceFactor(1, 7)).greaterThan(dissonanceFactor(0, 7));
  });
  test("Tritone more consonant than half step", () => {
    expect(dissonanceFactor(1, 2)).lessThan(dissonanceFactor(1, 7));
  });
  test("Octave more consonant than fifth", () => {
    expect(dissonanceFactor(0, 12)).lessThan(dissonanceFactor(0, 7));
  });
  test("Same note more consonant than octave", () => {
    expect(dissonanceFactor(0, 0)).lessThan(dissonanceFactor(0, 12));
  });
});

describe("Check chord dissonance", () => {
  test("cMajor vs bDim", () => {
    const cMajor = notesDissonance([
      { note: "C", octave: 0 },
      { note: "E", octave: 0 },
      { note: "G", octave: 0 },
    ]);
    const bDim = notesDissonance([
      { note: "B", octave: 0 },
      { note: "D", octave: 0 },
      { note: "F", octave: 0 },
    ]);
    expect(bDim).greaterThan(cMajor);
  });
  test("Major vs Minor", () => {
    const cMajor = notesDissonance([
      { note: "C", octave: 0 },
      { note: "E", octave: 0 },
      { note: "G", octave: 0 },
    ]);
    const cMinor = notesDissonance([
      { note: "C", octave: 0 },
      { note: "D#", octave: 0 },
      { note: "G", octave: 0 },
    ]);
    expect(cMinor).equals(cMajor);
  });
  test("Two chords one melody note", () => {
    const cMajor = notesDissonance([
      { note: "C", octave: 0 },
      { note: "E", octave: 0 },
      { note: "G", octave: 0 },
      { note: "B", octave: 0 }, // Melody note
    ]);
    const aMinor = notesDissonance([
      { note: "A", octave: 0 },
      { note: "C", octave: 0 },
      { note: "E", octave: 0 },
      { note: "B", octave: 0 }, // Melody note
    ]);
    expect(aMinor).lessThan(cMajor);
  });
  test("Two scales two possible chords on one note", () => {
    const dMinor = notesDissonance([
      { note: "D", octave: 0 },
      { note: "F", octave: 0 },
      { note: "A", octave: 0 },
    ]);
    const dMajor = notesDissonance([
      { note: "D", octave: 0 },
      { note: "F#", octave: 0 },
      { note: "A", octave: 0 },
    ]);
    expect(dMinor).equals(dMajor);
  });

  test("Two scales two possible chords on one note with melody", () => {
    const dMinor7 = notesDissonance([
      { note: "D", octave: 0 },
      { note: "F", octave: 0 },
      { note: "A", octave: 0 },
      { note: "C", octave: 0 }, // Melody note
    ]);
    const dMajor7 = notesDissonance([
      { note: "D", octave: 0 },
      { note: "F#", octave: 0 },
      { note: "A", octave: 0 },
      { note: "C", octave: 0 }, // Melody note
    ]);
    expect(dMajor7).greaterThan(dMinor7);
  });
  test("A sixth as a melody note vs a seventh", () => {
    const dMajor6 = notesDissonance([
      { note: "D", octave: 0 },
      { note: "F#", octave: 0 },
      { note: "A", octave: 0 },
      { note: "B", octave: 0 }, // Melody note
    ]);
    const dMajor7 = notesDissonance([
      { note: "D", octave: 0 },
      { note: "F#", octave: 0 },
      { note: "A", octave: 0 },
      { note: "C", octave: 0 }, // Melody note
    ]);
    expect(dMajor7).greaterThan(dMajor6);
  });
  test("A sixth as a melody note in major and minor", () => {
    const cMajor6 = notesDissonance([
      { note: "C", octave: 0 },
      { note: "E", octave: 0 },
      { note: "G", octave: 0 },
      { note: "A", octave: 0 }, // Melody note
    ]);
    const cMinor6 = notesDissonance([
      { note: "C", octave: 0 },
      { note: "D#", octave: 0 },
      { note: "G", octave: 0 },
      { note: "A", octave: 0 }, // Melody note
    ]);
    expect(cMinor6).greaterThan(cMajor6);
  });
});
