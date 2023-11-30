export const notes = [
  "B",
  "A#",
  "A",
  "G#",
  "G",
  "F#",
  "F",
  "E",
  "D#",
  "D",
  "C#",
  "C",
];

export const octaves = [5, 4, 3, 2, 1, 0];

export const tileWidth = 50;
export const gridMargin = 5;

export const baseApiUrl = import.meta.env.PROD
  ? "http://fs-21-sw-2-a313a.p2datsw.cs.aau.dk/node0"
  : "http://localhost:3280";

export const defaultVelocity = 0.1;
