# SDT Template Validator (JS)

Client-side validator for SDT template, rule, agent, project, execution, event, and billing specifications.

## Install
npm install

## Usage
```js
import {
  validateTemplate,
  validateRule,
  validateAgent,
  validateProject,
  validateExecution,
  validateEvent,
  validateBilling
} from "./validator";

validateTemplate(templateJson);
validateRule(ruleJson);
validateAgent(agentJson);
validateProject(projectJson);
validateExecution(executionJson);
validateEvent(eventJson);
validateBilling(billingJson);

```
This validator only checks structural validity.
Business logic, rewards, coins, and enforcement belong to the server.
