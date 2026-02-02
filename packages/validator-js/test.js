import assert from "assert";
import {
  validateProject,
  validateEvent,
} from "./validator.js";

function run(name, fn) {
  try {
    fn();
    console.log(`OK: ${name}`);
  } catch (err) {
    console.error(`FAIL: ${name}`);
    console.error(String(err));
    process.exitCode = 1;
  }
}

run("project dag cycle", () => {
  const project = {
    schema_version: "0.1.0",
    project_id: "proj_cycle",
    name: "Cyclic Project",
    owner_id: "user_1",
    agents: ["agent_a"],
    workflows: [
      {
        workflow_id: "wf_1",
        trigger: { type: "manual" },
        steps: [
          { step_id: "s1", agent_id: "agent_a", action: "capture", depends_on: ["s2"] },
          { step_id: "s2", agent_id: "agent_a", action: "capture", depends_on: ["s1"] },
        ],
      },
    ],
  };
  assert.throws(() => validateProject(project));
});

run("project unknown dependency", () => {
  const project = {
    schema_version: "0.1.0",
    project_id: "proj_dep",
    name: "Bad Dep Project",
    owner_id: "user_1",
    agents: ["agent_a"],
    workflows: [
      {
        workflow_id: "wf_1",
        trigger: { type: "manual" },
        steps: [
          { step_id: "s1", agent_id: "agent_a", action: "capture", depends_on: ["missing"] },
        ],
      },
    ],
  };
  assert.throws(() => validateProject(project));
});

run("event choice_made missing choice", () => {
  const event = {
    schema_version: "0.1.0",
    event_id: "evt_2",
    event_type: "choice_made",
    user_id: "user_1",
    project_id: "proj_1",
    timestamp: "2026-01-30T08:00:00Z",
  };
  assert.throws(() => validateEvent(event));
});

run("event field_changed missing field/value", () => {
  const event = {
    schema_version: "0.1.0",
    event_id: "evt_3",
    event_type: "field_changed",
    user_id: "user_1",
    project_id: "proj_1",
    timestamp: "2026-01-30T08:00:00Z",
  };
  assert.throws(() => validateEvent(event));
});

if (process.exitCode) {
  process.exit(1);
}
