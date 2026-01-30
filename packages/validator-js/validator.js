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
}

export function validateExecution(executionObj, { specDir } = {}) {
  validateAgainst("execution.schema.json", executionObj, "Execution", specDir);
}

export function validateEvent(eventObj, { specDir } = {}) {
  validateAgainst("event.schema.json", eventObj, "Event", specDir);
}

export function validateBilling(billingObj, { specDir } = {}) {
  validateAgainst("billing.schema.json", billingObj, "Billing", specDir);
}
