import { ToneAudioBuffer } from "tone";
import A3 from "./assets/samples/A3.flac";
import A4 from "./assets/samples/A4.flac";
import C4 from "./assets/samples/C4.flac";
import E4 from "./assets/samples/E4.flac";
import F4 from "./assets/samples/F4.flac";

export const samples = Object.fromEntries(
  Object.entries({ A3, A4, C4, E4, F4 }).map(([note, url]) => [
    note,
    new ToneAudioBuffer(url),
  ])
);
