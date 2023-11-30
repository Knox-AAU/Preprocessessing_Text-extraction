import * as Tone from "tone";
import { v4 as uuidv4 } from "uuid";
import { Project } from "../../shared/models";
import { getProject, newProject } from "./api";
import render, { ProjectState } from "./render";
import { samples } from "./sampleImport";
import { scheduleEvents } from "./scheduleEvents";
import "./style.css";

async function init() {
  // Remove right click menu
  window.addEventListener("contextmenu", (e) => e.preventDefault());

  document.body.onclick = async () => {
    // Tone should only start on user input
    await Tone.start();
    // Remove this eventlistener
    document.body.onclick = null;
  };
  const sampler = new Tone.Sampler({
    urls: samples,
  })
    .toDestination() // Decides main speakers as audio output
    .sync(); // Makes it so time is determined by the transport ("timeline")

  Tone.Transport.bpm.set({ value: 60 });

  const projectId = new URLSearchParams(window.location.search).get("project");
  const userId = getUserId();

  const project: Project | null = projectId
    ? await getProject(projectId)
    : await newProject(userId);
  if (project) {
    // Add the project id to the address bar
    window.history.replaceState(null, "", `?project=${project.id}`);

    scheduleEvents(sampler, project);

    // Used for the general state of the UI. Including the currently selected
    // track and state needed for dragging.
    const state: ProjectState = {
      project,
      selectedTrack: project.trackPair.melodyTrack,
      sampler,
    };
    render(state);
  } else {
    console.error(
      projectId ? "Could not get project" : "Could not create a new project"
    );
  }
}

function getUserId(): string {
  const key = "userId";
  const savedId = localStorage.getItem(key);
  if (!savedId) {
    // If the id does not exist, create one
    const generatedId = uuidv4();

    localStorage.setItem(key, generatedId);
    return generatedId;
  } else {
    return savedId;
  }
}

init();
