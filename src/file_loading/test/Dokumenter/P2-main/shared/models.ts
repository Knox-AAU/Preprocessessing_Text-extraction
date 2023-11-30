export type AttackRelease = {
  start: number; // Start and end are in sixteenths
  end: number;
  octaveNote: OctaveNote;
};

export type OctaveNote = {
  note: string;
  octave: number;
};

export type Project = {
  id: string;
  trackPair: TrackPair;
};

export type TrackPair = {
  melodyTrack: Track;
  chordTrack: Track;
};

export type Track = {
  type: "melody" | "chords";
  events: AttackRelease[];
};

export type User = {
  id: string;
  projects: string[]; // The ids of the projects the user created
};

export type NewProject = {
  userId: string;
};
