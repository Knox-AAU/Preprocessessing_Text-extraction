import * as Tone from "tone";
import { Sampler, Time, Transport } from "tone";
import { AttackRelease, OctaveNote, Project, Track } from "../../shared/models";
import { addEventAndSave, removeEventAndSave } from "./api";
import pauseIcon from "./assets/images/pauseLight.png";
import playIcon from "./assets/images/playLight.png";
import {
  defaultVelocity,
  gridMargin,
  notes,
  octaves,
  tileWidth,
} from "./constants";
import { getAllProjectEvents } from "./helpers/getAllProjectEvents";
import { getTracks } from "./helpers/getTracks";
import {
  getOctaveRowIndex as getOctaveNoteRowIndex,
  octaveNoteEquals,
  octaveNoteString,
} from "./helpers/octaveNotes";
import { samples } from "./sampleImport";
import { scheduleEvents } from "./scheduleEvents";
import {
  determineChordSuggestionForTime,
  determineSuggestionsForTime,
} from "./suggestions";

type DragStartEvent = Omit<AttackRelease, "end">;
type DragEndEvent = Omit<AttackRelease, "start">;

export type ProjectState = {
  project: Project;
  selectedTrack: Track;

  // An event without the end parameter
  dragStart?: DragStartEvent;
  // An event without the start parameter
  dragEnd?: DragEndEvent;

  // Column in the grid that was last hovered
  lastHover?: number;

  // Sampler to play instrument on timeline
  sampler: Sampler;
};

export default function render(state: ProjectState) {
  const timelineDiv = document.querySelector<HTMLDivElement>("#timeline")!;

  // Make sure the element is empty
  timelineDiv.innerHTML = "";

  const { timelineElement, gridElement, togglePlay, back } =
    createTimeline(state);

  // Wrapper element to make the timeline full height
  const timelineWrapper = document.createElement("div");
  timelineWrapper.className = "column full-height";
  timelineWrapper.appendChild(timelineElement);

  // Add the timeline to the document
  timelineDiv.appendChild(timelineWrapper);

  registerPlaybackButtons(togglePlay, back);

  populateTracksElement(state);

  // Register mouseup handler, which is used for adding and removing events
  document.addEventListener("mouseup", getMouseupHandler(state, gridElement));
}

function registerPlaybackButtons(togglePlay: () => void, back: () => void) {
  const playButton = document.getElementById(
    "play-button"
  )! as HTMLImageElement;
  playButton.onclick = () => {
    togglePlay();
    updatePlayButtonIcon(playButton);
  };
  updatePlayButtonIcon(playButton);

  const backButton = document.getElementById("back-button")!;
  backButton.onclick = () => {
    back();
    updatePlayButtonIcon(playButton);
  };
}

function populateTracksElement(state: ProjectState) {
  const tracksDiv = document.querySelector<HTMLDivElement>("#tracks")!;

  // Make sure the element is empty
  tracksDiv.innerHTML = "";

  tracksDiv.appendChild(
    createTrackElement("Melodi", state.project.trackPair.melodyTrack, state)
  );
  tracksDiv.appendChild(
    createTrackElement("Akkord", state.project.trackPair.chordTrack, state)
  );
}

function createTrackElement(
  name: string,
  track: Track,
  state: ProjectState
): HTMLDivElement {
  const trackElement = document.createElement("div");
  trackElement.innerText = name;
  trackElement.onclick = () => {
    changeTrack(state, track);
    populateTracksElement(state);
  };
  if (track === state.selectedTrack) {
    trackElement.classList.add("selected-track");
  }
  return trackElement;
}

function createTimeline(state: ProjectState) {
  // Left side tiles/grey squares with text are made
  const notesElement = createNotesElement();

  // Big grid, 1 column with many rows
  const gridElement = createTimelineGrid(state);

  // Sync scroll between the grid element and the notes element
  syncTimelineScroll(gridElement, notesElement);

  const timelineElement = document.createElement("div");
  timelineElement.className = "row gap flex-1 min-height";
  timelineElement.appendChild(notesElement);
  timelineElement.appendChild(gridElement);

  const cursorElement = createCursor(gridElement);
  timelineElement.appendChild(cursorElement);

  return {
    timelineElement,
    gridElement,
    togglePlay: () => {
      if (Transport.state === "started") {
        Transport.pause();
      } else {
        const { isBeforeScreen, isAfterScreen } =
          getCursorPositionDetails(gridElement);
        if (isBeforeScreen || isAfterScreen) {
          // Set cursor to start of screen if it isn't present on the screen
          Transport.position =
            (gridElement.scrollLeft / (tileWidth + gridMargin)) *
            Time("16n").toSeconds();
        }
        Transport.start();
      }
    },
    back: () => {
      Transport.stop();
      gridElement.scrollTo({ left: 0 });
    },
  };
}

function createTimelineGrid(state: ProjectState) {
  const gridElement = document.createElement("div");
  gridElement.id = "grid-element";
  gridElement.className = "column gap scroll flex-1 min-width";

  // Cycles all the rows in the timeline
  octaves.forEach((octave) => {
    notes.forEach((note) => {
      const rowElement = document.createElement("div");
      rowElement.className = "row gap";

      // Creates 2^8 tiles per row, means tracks can be this long
      for (let tileTime = 0; tileTime < 2 ** 8; tileTime++) {
        const tile = document.createElement("div");
        const octaveNote = { note, octave };

        tile.onmouseenter = () => {
          // Only do something is the user is dragging
          if (state.dragStart) {
            // Updates the dragging end value to the current tile
            state.dragEnd = { end: tileTime + 1, octaveNote };
            colorTilesInRow({
              gridElement,
              state,
              octaveNote: state.dragStart.octaveNote,
            });
          }
          colorSuggestionsInColumn(state, tileTime, gridElement, octaveNote);
          state.lastHover = tileTime;
        };

        tile.onmousedown = () => {
          // Initializes the dragging values
          state.dragStart = { octaveNote, start: tileTime };
          state.dragEnd = { octaveNote, end: tileTime + 1 };

          colorTilesInRow({
            gridElement,
            state,
            octaveNote: state.dragStart.octaveNote,
          });
        };
        rowElement.appendChild(tile);
      }

      gridElement.appendChild(rowElement);
    });
  });

  // Color the tiles in the grid element
  colorGridTiles(gridElement, state);

  return gridElement;
}

// Sync the vertical scroll of gridElement and notesElement
function syncTimelineScroll(
  gridElement: HTMLDivElement,
  notesElement: HTMLDivElement
) {
  gridElement.addEventListener("scroll", () => {
    notesElement.scrollTo(0, gridElement.scrollTop);
  });
  notesElement.addEventListener("scroll", () => {
    gridElement.scrollTo(gridElement.scrollLeft, notesElement.scrollTop);
  });
}

function getMouseupHandler(
  state: ProjectState,
  gridElement: HTMLDivElement
): (e: MouseEvent) => void {
  return () => {
    if (!state.dragStart || !state.dragEnd) return;

    const eventDeleted = tryDeleteEvent(state);

    if (!eventDeleted) {
      // Sampler for sounds played on click
      const clickSampler = new Tone.Sampler({
        urls: samples,
      }).toDestination();

      if (state.selectedTrack.type === "melody") {
        handleMelodyAddEvent(state, clickSampler);
      } else {
        handleChordAddEvents(state, gridElement, clickSampler);
      }
    }

    scheduleEvents(state.sampler, state.project);

    // Save octave note and row element before dragging fields are reset
    const octaveNote = state.dragStart.octaveNote;

    // Redraw without dragging
    resetDragging(state);
    colorTilesInRow({
      octaveNote,
      gridElement,
      state,
    });

    // Redraw suggestions based on the new event
    if (state.lastHover !== undefined) {
      colorSuggestionsInColumn(state, state.lastHover, gridElement, octaveNote);
    }
  };
}

function handleMelodyAddEvent(state: ProjectState, clickSampler: Tone.Sampler) {
  if (!state.dragStart || !state.dragEnd) return;

  const eventAdded = addEventIfLegal(
    state.dragStart,
    state.dragEnd,
    state.selectedTrack,
    state.project
  );

  if (eventAdded) {
    // Plays sound when note is clicked
    clickSampler.triggerAttackRelease(
      octaveNoteString(state.dragStart.octaveNote),
      "16n",
      undefined,
      0.1
    );
  }
}

function handleChordAddEvents(
  state: ProjectState,
  gridElement: HTMLDivElement,
  clickSampler: Tone.Sampler
) {
  if (!state.dragStart || !state.dragEnd) return;

  const chordSuggestion = determineChordSuggestionForTime(
    state.dragStart.start,
    state.project,
    state.selectedTrack,
    state.dragStart.octaveNote
  );

  if (chordSuggestion) {
    for (const { note, octave } of chordSuggestion) {
      addEventIfLegal(
        { ...state.dragStart, octaveNote: { note, octave } },
        state.dragEnd,
        state.selectedTrack,
        state.project
      );
      // Make sure all the rows are colored correctly
      colorTilesInRow({
        octaveNote: { octave, note },
        gridElement,
        state,
      });
    }

    const notesToPlay = getAllProjectEvents(state.project)
      .filter((e) => e.start === state.dragStart!.start)
      .map((e) => octaveNoteString(e.octaveNote));

    clickSampler.triggerAttackRelease(
      notesToPlay,
      "16n",
      undefined,
      defaultVelocity
    );
  }
}

// Resets the dragging events to be undefined
function resetDragging(state: ProjectState) {
  state.dragStart = undefined;
  state.dragEnd = undefined;
}

function tryDeleteEvent(state: ProjectState): boolean {
  if (!state.dragStart || !state.dragEnd) return false;

  const dragStartNote = state.dragStart.octaveNote;
  const dragEndNote = state.dragEnd.octaveNote;

  // Find an event that should be deleted.
  const deleteIndex = state.selectedTrack.events.findIndex(
    (e) =>
      octaveNoteEquals(e.octaveNote, dragStartNote) &&
      e.start === state.dragStart!.start &&
      // Ensure that dragStart and dragEnd is on the same tile
      e.start + 1 === state.dragEnd?.end &&
      octaveNoteEquals(e.octaveNote, dragEndNote)
  );
  if (deleteIndex !== -1) {
    // Found something to delete
    removeEventAndSave(state.project, state.selectedTrack, deleteIndex);
    scheduleEvents(state.sampler, state.project);
    return true;
  }
  return false;
}

function createNotesElement() {
  const notesElement = document.createElement("div");
  notesElement.className = "column gap scroll";
  octaves.forEach(() => {
    notes.forEach((note) => {
      // 12 notes from a to g in each octave
      const noteTile = document.createElement("div"); // The grey squares
      noteTile.className = "tile";

      if (note.includes("#")) {
        // Adds 'sharp' class for css/styling purpose to 'halftones'
        noteTile.classList.add("sharp");
      } else {
        // The text in the grey squares
        noteTile.innerText = note;
      }

      notesElement.appendChild(noteTile);
    });
  });
  return notesElement;
}

function createCursor(gridElement: HTMLDivElement) {
  const cursorElement = document.createElement("div");
  cursorElement.className = "cursor";

  // Rendering loop that gets called for each animation frame
  function cursorRenderingLoop() {
    requestAnimationFrame(cursorRenderingLoop);

    // Bounding rect of the timeline grid
    const rect = gridElement.getBoundingClientRect();

    const { isBeforeScreen, isAfterScreen, position } =
      getCursorPositionDetails(gridElement);

    // When the cursor plays out of the screen
    if (isAfterScreen && Transport.state === "started") {
      // Scroll an entire screen to the right
      gridElement.scrollBy({ left: rect.width });
    }

    // Only display when cursor is inside the timeline
    cursorElement.style.display =
      isBeforeScreen || isAfterScreen ? "none" : "block";

    // Position and size the cursor
    cursorElement.style.left = `${position}px`;
    cursorElement.style.top = `${rect.top}px`;
    cursorElement.style.height = `${rect.height}px`;
  }
  // Start the rendering loop
  cursorRenderingLoop();

  return cursorElement;
}

function getCursorPositionDetails(gridElement: HTMLDivElement) {
  // An object holding the coordinates of the gridElement bounds
  const rect = gridElement.getBoundingClientRect();
  // The time in notes converted from the BPM independent unit "ticks"
  const time = Time(Transport.position).toTicks() / Time("16n").toTicks();
  // x position in the grid based on the time (pixels)
  const offset = time * (tileWidth + gridMargin);
  // The x position of the cursor
  const left = rect.left - gridElement.scrollLeft + offset;

  // Determine if the cursor is outside of the screen
  const isAfterScreen = left + 2 > rect.left + rect.width;
  const isBeforeScreen = left < rect.left;

  return { isBeforeScreen, isAfterScreen, position: left };
}

function addEventIfLegal(
  dragStart: DragStartEvent,
  dragEnd: DragEndEvent,
  selectedTrack: Track,
  project: Project
): boolean {
  if (dragStart.start < dragEnd.end) {
    // Combines dragEnd and dragStart into a complete event
    const newEvent: AttackRelease = { ...dragEnd, ...dragStart };
    const eventWithOverlap = selectedTrack.events.find(
      (e) =>
        octaveNoteEquals(e.octaveNote, newEvent.octaveNote) &&
        eventsHasTimeOverlap(newEvent, e)
    );
    if (!eventWithOverlap) {
      addEventAndSave(project, selectedTrack, newEvent);
      return true;
    }
  }
  return false;
}

// Determines if two events overlaps in time
function eventsHasTimeOverlap(
  newEvent: AttackRelease,
  existingEvent: AttackRelease
): boolean {
  // The following comments describes the possible cases for overlap of two
  // events. Where "|---------|" is the existing event and "I---------I" is the
  // events that we're trying to insert.
  return (
    // -----I------|---I-----|--------------
    (newEvent.start <= existingEvent.start &&
      newEvent.end - 1 >= existingEvent.start) ||
    // ------------|-----I---|-------I------
    (newEvent.start <= existingEvent.end - 1 &&
      newEvent.end >= existingEvent.end) ||
    // ------------|-I-----I-|--------------
    (newEvent.start >= existingEvent.start && newEvent.end <= existingEvent.end)
  );
}

// Updates the colors of the tiles in the row
function colorTilesInRow({
  octaveNote: { note, octave },
  gridElement,
  state: { dragStart, dragEnd, selectedTrack, project },
}: {
  octaveNote: OctaveNote;
  gridElement: HTMLDivElement;
  state: ProjectState;
}) {
  const isSharp = note.includes("#");

  const rowFilter = (e: AttackRelease) =>
    e.octaveNote.note === note && e.octaveNote.octave === octave;
  const rowEvents = selectedTrack.events.filter(rowFilter);
  const anyTrackRowEvents = getTracks(project)
    .filter((t) => t !== selectedTrack)
    .flatMap((t) => t.events.filter(rowFilter));

  const getStartTime = (e: AttackRelease) => e.start;
  const selected = new Set(rowEvents.map(getStartTime));
  const anyTrackSelected = new Set(anyTrackRowEvents.map(getStartTime));

  const getEventTimeRangeIndicies = (e: AttackRelease) => {
    const result: number[] = [];
    for (let i = e.start + 1; i < e.end; i++) {
      result.push(i);
    }
    return result;
  };
  const selectedDrag = new Set(rowEvents.flatMap(getEventTimeRangeIndicies));
  const anyTrackSelectedDrag = new Set(
    anyTrackRowEvents.flatMap(getEventTimeRangeIndicies)
  );

  const rowElement = gridElement.children.item(
    getOctaveNoteRowIndex({ note, octave })
  )!;

  const shouldShowDrag = dragStart && dragEnd && dragStart.start < dragEnd.end;
  if (shouldShowDrag) {
    selected.add(dragStart.start);
    getEventTimeRangeIndicies({ ...dragEnd, ...dragStart }).forEach((i) =>
      selectedDrag.add(i)
    );
  }

  rowElement.childNodes.forEach((t, i) => {
    const tile = t as HTMLDivElement;

    // Object that maps class names to a boolean value of weather the class
    // should be applied to the tile.
    const classes: Record<string, boolean> = {
      tile: true,
      sharp: isSharp,
      selected: selected.has(i),
      "selected-drag": selectedDrag.has(i),
      "any-selected": anyTrackSelected.has(i),
      "any-selected-drag": anyTrackSelectedDrag.has(i),
    };

    // Update classes with the entries from the object that has a true value
    tile.className = "";
    tile.classList.add(
      ...Object.entries(classes)
        .filter(([, shouldHaveClass]) => shouldHaveClass)
        .map(([name]) => name)
    );
  });
}

// Updates the icon of playButton based on the state of the Transport
function updatePlayButtonIcon(playButton: HTMLImageElement) {
  if (Transport.state === "started") {
    playButton.src = pauseIcon;
  } else {
    playButton.src = playIcon;
  }
}

// Color note suggestions for a single column in the grid
function colorSuggestionsInColumn(
  state: ProjectState,
  time: number,
  gridElement: HTMLDivElement,
  octaveNote: OctaveNote
) {
  const suggestion = determineSuggestionsForTime(
    time,
    state.project,
    state.selectedTrack,
    octaveNote
  );
  const rowElements = gridElement.children;
  octaves.forEach((octave) => {
    notes.forEach((note) => {
      const rowElement = rowElements[getOctaveNoteRowIndex({ octave, note })];
      if (state.lastHover !== undefined) {
        const lastHoverTile = rowElement.children[state.lastHover];
        // Remove suggestions from last hover
        lastHoverTile.classList.remove("suggestion");
      }

      const tile = rowElement.children[time];
      if (suggestion.has(note) || suggestion.has(note + octave)) {
        // Add class to the tile which note is part of the suggested notes
        tile.classList.add("suggestion");
      }
    });
  });
}

function changeTrack(state: ProjectState, track: Track) {
  state.selectedTrack = track;
  state.lastHover = undefined;
  const gridElement = document.querySelector<HTMLDivElement>("#grid-element");
  if (!gridElement) {
    throw "Grid element should be present when changing tracks";
  }
  // Recolor the tiles in the grid to accommodate that the selected track has
  // been changed
  colorGridTiles(gridElement, state);
}

function colorGridTiles(gridElement: HTMLDivElement, state: ProjectState) {
  octaves.forEach((octave) => {
    notes.forEach((note) => {
      colorTilesInRow({
        octaveNote: { note, octave },
        gridElement,
        state,
      });
    });
  });
}
