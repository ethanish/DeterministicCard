import fs from "fs";
import path from "path";
import Ajv from "ajv";
import addFormats from "ajv-formats";

function defaultSpecDir() {
  return path.resolve(process.cwd(), "spec");
}

function loadSchemas(specDir) {
  const dir = specDir || defaultSpecDir();
  const files = fs.readdirSync(dir).filter((f) => f.endsWith(".json"));
  const schemas = [];
  for (const file of files) {
    const full = path.join(dir, file);
    const schema = JSON.parse(fs.readFileSync(full, "utf-8"));
    schemas.push(schema);
  }
  return { dir, schemas };
}

function buildAjv(specDir) {
  const ajv = new Ajv({ allErrors: true, strict: false });
  addFormats(ajv);
  const { schemas } = loadSchemas(specDir);
  for (const schema of schemas) {
    ajv.addSchema(schema, schema.$id || schema.title);
  }
  return ajv;
}

function validateAgainst(schemaFile, obj, label, specDir) {
  const ajv = buildAjv(specDir);
  const schemaPath = path.join(specDir || defaultSpecDir(), schemaFile);
  if (!fs.existsSync(schemaPath)) {
    throw new Error(`Schema file not found: ${schemaPath}`);
  }
  const schema = JSON.parse(fs.readFileSync(schemaPath, "utf-8"));
  const validate = ajv.compile(schema);
  const valid = validate(obj);
  if (!valid) {
    const errors = (validate.errors || []).map((e) => {
      const where = e.instancePath ? ` at '${e.instancePath}'` : "";
      return `${e.message}${where}`;
    });
    const detail = errors.length ? `\n${errors.map((e) => `- ${e}`).join("\n")}` : "";
    throw new Error(`${label} failed schema validation.${detail}`);
  }
}

function validateProjectWorkflowDag(projectObj) {
  const errors = [];
  const workflows = projectObj.workflows || [];
  workflows.forEach((workflow, wIdx) => {
    const steps = workflow.steps || [];
    const stepIds = steps.map((s) => s.step_id).filter(Boolean);
    const stepIdSet = new Set(stepIds);
    if (stepIds.length !== stepIdSet.size) {
      errors.push(`Workflow[${wIdx}] has duplicate step_id values.`);
      return;
    }

    const edges = {};
    stepIds.forEach((id) => {
      edges[id] = [];
    });
    steps.forEach((step, sIdx) => {
      const stepId = step.step_id;
      if (!stepId) return;
      const deps = step.depends_on || [];
      deps.forEach((dep) => {
        if (!stepIdSet.has(dep)) {
          errors.push(
            `Workflow[${wIdx}].steps[${sIdx}].depends_on references unknown step_id '${dep}'.`
          );
          return;
        }
        edges[dep].push(stepId);
      });
    });

    const visiting = new Set();
    const visited = new Set();
    function dfs(node) {
      if (visiting.has(node)) return true;
      if (visited.has(node)) return false;
      visiting.add(node);
      for (const nxt of edges[node] || []) {
        if (dfs(nxt)) return true;
      }
      visiting.delete(node);
      visited.add(node);
      return false;
    }

    for (const node of stepIdSet) {
      if (dfs(node)) {
        errors.push(`Workflow[${wIdx}] has a dependency cycle.`);
        break;
      }
    }
  });

  if (errors.length) {
    const detail = `\n${errors.map((e) => `- ${e}`).join("\n")}`;
    throw new Error(`Project failed workflow DAG validation.${detail}`);
  }
}

function validateEventTypeFields(eventObj) {
  const errors = [];
  const eventType = eventObj.event_type;

  if (eventType === "choice_made") {
    if (typeof eventObj.choice !== "object" || eventObj.choice === null) {
      errors.push("Event.choice must be provided for event_type 'choice_made'.");
    }
  } else if (eventType === "field_changed") {
    if (eventObj.field == null) {
      errors.push("Event.field must be provided for event_type 'field_changed'.");
    }
    if (!Object.prototype.hasOwnProperty.call(eventObj, "value")) {
      errors.push("Event.value must be provided for event_type 'field_changed'.");
    }
  } else if (eventType === "session_end") {
    // No extra required fields currently.
  }

  if (errors.length) {
    const detail = `\n${errors.map((e) => `- ${e}`).join("\n")}`;
    throw new Error(`Event failed event_type field validation.${detail}`);
  }
}

export function validateTemplate(templateObj, { specDir } = {}) {
  validateAgainst("template.schema.json", templateObj, "Template", specDir);
}

export function validateRule(ruleObj, { specDir } = {}) {
  validateAgainst("rule.schema.json", ruleObj, "Rule", specDir);
}

export function validateAgent(agentObj, { specDir } = {}) {
  validateAgainst("agent.schema.json", agentObj, "Agent", specDir);
}

export function validateProject(projectObj, { specDir } = {}) {
  validateAgainst("project.schema.json", projectObj, "Project", specDir);
  validateProjectWorkflowDag(projectObj);
}

export function validateExecution(executionObj, { specDir } = {}) {
  validateAgainst("execution.schema.json", executionObj, "Execution", specDir);
}

export function validateEvent(eventObj, { specDir } = {}) {
  validateAgainst("event.schema.json", eventObj, "Event", specDir);
  validateEventTypeFields(eventObj);
}

export function validateBilling(billingObj, { specDir } = {}) {
  validateAgainst("billing.schema.json", billingObj, "Billing", specDir);
}
