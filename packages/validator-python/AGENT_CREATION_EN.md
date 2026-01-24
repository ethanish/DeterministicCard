# Agent Creation Guide: Creating a New Agent via CLI

## 1. Philosophy

### 1.1 Self-Determination Theory (SDT) Based Design Philosophy

This CLI tool is designed based on the core principles of **Self-Determination Theory (SDT)**. SDT emphasizes three fundamental psychological needs for human intrinsic motivation and growth:

- **Autonomy**: The freedom for users to choose their own goals and meaning
- **Competence**: The ability for users to recognize growth they define themselves
- **Relatedness**: Optional, non-coercive connection and sharing

### 1.2 The Philosophical Meaning of Agent Creation

Creating an agent is not simply about creating a technical JSON file. It is:

1. **Structure, Not Control**: Agents provide structure to users, but users decide how to use that structure.
2. **Tool for Growth**: Agents are tools that enable users to track and reflect on their own growth.
3. **Freedom of Choice**: Users can modify or disable agents at any time.

### 1.3 The Meaning of "An Agent Creating a New Agent"

When we create an agent by running this CLI, we:

- **Template-Based Consistency**: Maintain consistent structure by referencing existing templates.
- **Autonomy Through Validation**: Ensure users have chosen the correct structure through schema validation.
- **Extensible Design**: Users can add or modify capabilities according to their needs.

## 2. Accurate Todo Checklist

### 2.1 Pre-Preparation Phase

#### To Do
- [ ] Review and select template file (must comply with `template.schema.json`)
- [ ] Clearly define the agent's purpose and role
- [ ] Determine which SDT elements the agent will support (autonomy, competence, relatedness)
- [ ] Determine required capability types (capture, suggest, remind, analyze, custom)
- [ ] Plan mapping between template fields and agent capabilities

#### Done
- [ ] Template ID confirmed
- [ ] Agent ID and name decided
- [ ] JSON editor or text editor prepared

### 2.2 Agent JSON File Writing Phase

#### To Do
- [ ] Write required fields: `id`, `name`, `template_id`
- [ ] Write optional fields: `description`
- [ ] Write `capabilities` array (each capability includes type-specific required fields)
- [ ] Write `sdt_support` object (descriptions for autonomy, competence, relatedness)
- [ ] Set `enabled` field (default: true)

#### Done
- [ ] All required fields written
- [ ] No JSON syntax errors confirmed
- [ ] Template fields and capability field references match confirmed

### 2.3 Validation Phase

#### To Do
- [ ] Run CLI command: `sdt-validate agent <agent_file.json>`
- [ ] Validate with template file: `sdt-validate agent <agent_file.json> --template <template_file.json>`
- [ ] Fix validation errors (if any)
- [ ] Confirm final validation passes

#### Done
- [ ] Schema validation passed ("OK" output confirmed)
- [ ] Template reference validation passed
- [ ] All capability field reference validity confirmed

### 2.4 Deployment and Usage Phase

#### To Do
- [ ] Save agent file to appropriate location
- [ ] Integrate agent into application that will use it
- [ ] Collect user testing and feedback
- [ ] Modify and re-validate agent if necessary

#### Done
- [ ] Agent file deployed
- [ ] Application integration completed
- [ ] Initial testing completed

## 3. Detailed Design Explanation Aligned with Self-Determination Theory

### 3.1 Autonomy Support Design

#### 3.1.1 Structural Autonomy

Agent design **provides structure but does not control** users:

```json
{
  "capabilities": [
    {
      "type": "capture",
      "field": "reflection",
      "trigger": "manual"  // User directly chooses
    }
  ]
}
```

- **Trigger Options**: `manual`, `on_field_change`, `on_time_interval`, `on_session_end`, `on_condition_met`
- Users can always choose `trigger: "manual"` to have complete control.
- Setting `enabled: false` allows complete deactivation of the agent.

#### 3.1.2 Freedom of Choice

- **Capability Selection**: Users select only the capabilities they need to compose the agent.
- **SDT Support Selection**: Users can choose which SDT elements to emphasize in the `sdt_support` object.
- **Field Mapping**: Users don't need to use all template fields; only map necessary fields to capabilities.

#### 3.1.3 Autonomy Through Validation

The CLI validation process:

1. **Structure Validation**: Ensures compliance with JSON schema to prevent technical errors.
2. **Reference Validation**: Confirms consistency with templates to ensure the agent works as intended.
3. **No Coercion**: Validation does not enforce "correct" usage, only checks structural consistency.

### 3.2 Competence Support Design

#### 3.2.1 Growth Tracking Capability

Agents are designed to track growth defined by users:

```json
{
  "capabilities": [
    {
      "type": "analyze",
      "field": "session_length",
      "trigger": "on_time_interval",
      "config": {
        "model": "trend_analysis",
        "parameters": {
          "window": "7d"
        }
      }
    }
  ],
  "sdt_support": {
    "competence": "Analyzes trends in user-defined session length to visualize growth."
  }
}
```

- **Analyze Capability**: Analyzes user data to discover patterns and trends.
- **User-Defined Metrics**: Tracks growth indicators defined by users in conjunction with template `metrics`.

#### 3.2.2 Immediate Feedback

- **Suggest Capability**: Provides immediate suggestions based on user input.
- **Remind Capability**: Reminds users of growth at intervals they set.

#### 3.2.3 Transparent Operation

- **Clear Description**: `description` and `sdt_support` clearly explain how the agent works.
- **Predictability**: Through triggers and config, users can predict when and how the agent operates.

### 3.3 Relatedness Support Design

#### 3.3.1 Optional Sharing

```json
{
  "sdt_support": {
    "relatedness": "Users can optionally share reflections. This is not forced."
  }
}
```

- **Optional Fields**: Utilizes template `optional: true` fields to make sharing optional.
- **Manual Trigger**: Sharing-related capabilities use `trigger: "manual"` to give users complete control.

#### 3.3.2 Non-Coercive Connection

- Agents **support** relatedness but **do not force** it.
- `sdt_support.relatedness` is descriptive only, not a required feature.

### 3.4 Integrated Design Principles

#### 3.4.1 Template-Based Consistency

Agents must reference a template (`template_id`). This provides:

- **Structural Consistency**: Maintains consistency among multiple agents using the same template
- **Extensibility**: Modifying a template can affect all agents using that template
- **Validatability**: Validates references between templates and agents to prevent errors

#### 3.4.2 Modularization of Capabilities

Each capability operates independently, and users can select only what they need:

- **Capture**: Data collection
- **Suggest**: Suggestion provision
- **Remind**: Notification provision
- **Analyze**: Analysis performance
- **Custom**: User-defined functionality

#### 3.4.3 SDT Alignment of Validation Process

The CLI validation process itself follows SDT principles:

1. **Autonomy**: Validation does not enforce "correct" usage, only checks structural consistency.
2. **Competence**: Validation ensures the agent will work as the user intended.
3. **Relatedness**: Template reference validation ensures consistency with other components.

### 3.5 Practical Usage Examples

#### Example 1: Game Growth Tracking Agent

```json
{
  "id": "game-growth-agent-001",
  "name": "Game Session Analysis Agent",
  "template_id": "game-growth-basic",
  "description": "Analyzes player game sessions and provides growth trends.",
  "capabilities": [
    {
      "type": "capture",
      "field": "session_length",
      "trigger": "on_session_end"
    },
    {
      "type": "analyze",
      "field": "session_length",
      "trigger": "on_time_interval",
      "config": {
        "model": "trend",
        "parameters": {
          "interval": "7d"
        }
      }
    },
    {
      "type": "suggest",
      "field": "difficulty",
      "trigger": "on_field_change",
      "config": {
        "max_suggestions": 3
      }
    }
  ],
  "sdt_support": {
    "autonomy": "Players freely choose difficulty and session length.",
    "competence": "Analyzes session length trends to show player persistence improvement.",
    "relatedness": "Players can optionally share reflections."
  },
  "enabled": true
}
```

This agent:
- **Autonomy**: Players choose difficulty, and reflection is optional.
- **Competence**: Shows growth through session length trend analysis.
- **Relatedness**: Supports optional reflection sharing.

#### Example 2: Learning Tracking Agent

```json
{
  "id": "learning-agent-001",
  "name": "Learning Progress Reminder Agent",
  "template_id": "learning-basic",
  "description": "Tracks learner progress and provides periodic reminders.",
  "capabilities": [
    {
      "type": "remind",
      "field": "study_time",
      "trigger": "on_time_interval",
      "config": {
        "interval": "1d",
        "message": "Please record today's study time."
      }
    },
    {
      "type": "capture",
      "field": "study_time",
      "trigger": "manual"
    }
  ],
  "sdt_support": {
    "autonomy": "Learners freely choose when and how much to study.",
    "competence": "Supports continuous learning habit formation through study time tracking.",
    "relatedness": "Learners can optionally share progress with study groups."
  },
  "enabled": true
}
```

## 4. CLI Usage Summary

### 4.1 Basic Validation

```bash
sdt-validate agent my_agent.json
```

### 4.2 Validation with Template (Recommended)

```bash
sdt-validate agent my_agent.json --template my_template.json
```

### 4.3 Using Custom Spec Directory

```bash
sdt-validate agent my_agent.json --spec-dir /path/to/spec
```

### 4.4 On Validation Success

```
OK
```

### 4.5 On Validation Failure

Detailed error messages with specific issues are output. Fix them and validate again.

## 5. Conclusion

The process of creating an agent using this CLI is not a simple technical task. It is about creating a tool that supports user autonomy, competence, and relatedness according to Self-Determination Theory principles.

While ensuring structural consistency through the validation process, users can freely compose and modify agents according to their needs. This is the implementation of the "structure, not control" design philosophy.
