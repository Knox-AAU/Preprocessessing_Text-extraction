import { OctaveNote } from "../../shared/models";
import { notes, octaves } from "./constants";

export function notesDissonance(octaveNotes: OctaveNote[]): number {
  const reversedNotes = getReversedArray(notes);
  const reversedOctaves = getReversedArray(octaves);
  const noteIndecies = octaveNotes.map(
    ({ note, octave }) =>
      reversedNotes.indexOf(note) +
      reversedOctaves.indexOf(octave) * notes.length
  );
  const indexPairs = noteIndecies.flatMap((i) =>
    noteIndecies.map((j) => [i, j])
  );

  const dissonances = indexPairs.map(([origin, destination]) => {
    const df = dissonanceFactor(origin, destination);
    return df;
  });
  const cumulativeDissonances = dissonances.reduce((a, b) => a + b, 0);
  return cumulativeDissonances;
}

// Source:
// https://upcommons.upc.edu/bitstream/handle/2099/8052/article2.pdf?sequence=1
export function dissonanceFactor(origin: number, destination: number) {
  const ratio = ratioBetween(origin, destination);
  // The size of this can determine how dissonant an interval is
  return Math.log(lcm(ratio.num, ratio.den));
}

// Source:
// https://stackoverflow.com/questions/31302054/
export function lcm(a: number, b: number): number {
  return (a * b) / gcd(a, b);
}
export function gcd(a: number, b: number): number {
  return !b ? a : gcd(b, a % b);
}

function getReversedArray<T>(array: T[]): T[] {
  const reverseArray = [...array];
  return reverseArray.reverse();
}

export function ratioBetween(origin: number, destination: number) {
  const upRatio = findRatio({ num: 3, den: 2 }, 7, origin, destination);
  const downRatio = findRatio({ num: 2, den: 3 }, -7, origin, destination);
  return upRatio.den < downRatio.den ? upRatio : downRatio;
}

type Fraction = { num: number; den: number };

export function findRatio(
  jumpFraction: Fraction,
  jumpDistance: number,
  origin: number,
  destination: number
): Fraction {
  // How many steps you must go up (or down) to get to the fifth in TET
  const notesPerOctave = 12;
  const octaveRatio = 2;

  let distance: number = Math.abs(destination - origin);
  // Edge case for the octave
  if (distance % notesPerOctave === 0) {
    const octaves = Math.pow(2, distance / notesPerOctave);
    return { num: octaves, den: 1 };
  }
  distance = distance % notesPerOctave;

  const relativeFraction: Fraction = { num: 1, den: 1 };
  let notesFromOrigin = 0;
  //Loop runs until the note reaches the desired point
  while (notesFromOrigin !== distance) {
    //Jumps up a fifth both in frequency and in note index
    relativeFraction.num *= jumpFraction.num;
    relativeFraction.den *= jumpFraction.den;
    notesFromOrigin += jumpDistance;
    // If the note exceeds an octave, go back one octave
    if (notesFromOrigin > notesPerOctave) {
      relativeFraction.den *= octaveRatio;
      notesFromOrigin -= notesPerOctave;
    } else if (notesFromOrigin < 0) {
      relativeFraction.num *= octaveRatio;
      notesFromOrigin += notesPerOctave;
    }
  }
  return { num: relativeFraction.num, den: relativeFraction.den };
}

// These comments explain the example of finding the ratio between
// C (with index 0) and D (with index 2)

// We want to find the note interval between the two notes C and D
// https://i.imgur.com/8WXGBOT.png

// In this algorithm we only know how to move in fifths
// Therefore the first step goes from C to G
// The algorithm checks if this is the right note
// It is not, sice the distance from C to G is 7 but we want a distance of 2.
// https://i.imgur.com/s4YVniU.png

// We jump forth one more fifth and land at D
// This D is, however an octave too high
// https://i.imgur.com/TxuPkl9.png

//Therefore it goes back and octave and happens to land on the right D and the
//loop terminates
// https://i.imgur.com/OSBV1XD.png
