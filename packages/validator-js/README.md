# SDT Template Validator (JS)

Client-side validator for SDT template and rule specifications.

## Install
npm install

## Usage
```js
import { validateTemplate, validateRule } from "./validator";

validateTemplate(templateJson);
validateRule(ruleJson);

```
This validator only checks structural validity.
Business logic, rewards, coins, and enforcement belong to the server.
