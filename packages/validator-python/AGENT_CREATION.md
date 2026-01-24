# 에이전트 생성 가이드: CLI를 통한 새로운 에이전트 만들기

## 1. 철학

### 1.1 Self-Determination Theory (SDT) 기반 설계 철학

이 CLI 도구는 **Self-Determination Theory (자기결정성 이론)**의 핵심 원칙에 기반하여 설계되었습니다. SDT는 인간의 내재적 동기와 성장을 위한 세 가지 기본 심리적 욕구를 강조합니다:

- **자율성 (Autonomy)**: 사용자가 자신의 목표와 의미를 선택할 수 있는 자유
- **유능감 (Competence)**: 사용자가 정의한 성장을 스스로 인식할 수 있는 능력
- **관계성 (Relatedness)**: 선택적이고 강제되지 않는 연결과 공유

### 1.2 에이전트 생성의 철학적 의미

에이전트를 생성한다는 것은 단순히 기술적인 JSON 파일을 만드는 것이 아닙니다. 그것은:

1. **구조 제공, 통제가 아닌**: 에이전트는 사용자에게 구조를 제공하지만, 그 구조를 어떻게 사용할지는 사용자가 결정합니다.
2. **성장의 도구**: 에이전트는 사용자가 자신의 성장을 추적하고 반영할 수 있는 도구입니다.
3. **선택의 자유**: 사용자는 언제든지 에이전트를 수정하거나 비활성화할 수 있습니다.

### 1.3 "에이전트가 새로운 에이전트를 만든다"의 의미

이 CLI를 실행하여 에이전트를 생성할 때, 우리는:

- **템플릿 기반의 일관성**: 기존 템플릿을 참조하여 일관된 구조를 유지합니다.
- **검증을 통한 자율성 보장**: 스키마 검증을 통해 사용자가 올바른 구조를 선택했는지 확인합니다.
- **확장 가능한 설계**: 사용자는 자신의 필요에 맞게 capabilities를 추가하거나 수정할 수 있습니다.

## 2. 정확한 Todo Checklist

### 2.1 사전 준비 단계

#### 할 일 (To Do)
- [ ] 템플릿 파일 확인 및 선택 (`template.schema.json` 준수)
- [ ] 에이전트의 목적과 역할 명확히 정의
- [ ] 에이전트가 지원할 SDT 요소 결정 (autonomy, competence, relatedness)
- [ ] 필요한 capabilities 타입 결정 (capture, suggest, remind, analyze, custom)
- [ ] 템플릿의 fields와 에이전트 capabilities 간 매핑 계획

#### 완료 확인 (Done)
- [ ] 템플릿 ID 확인 완료
- [ ] 에이전트 ID 및 이름 결정 완료
- [ ] JSON 에디터 또는 텍스트 에디터 준비 완료

### 2.2 에이전트 JSON 파일 작성 단계

#### 할 일 (To Do)
- [ ] 필수 필드 작성: `id`, `name`, `template_id`
- [ ] 선택적 필드 작성: `description`
- [ ] `capabilities` 배열 작성 (각 capability는 타입별 필수 필드 포함)
- [ ] `sdt_support` 객체 작성 (autonomy, competence, relatedness 설명)
- [ ] `enabled` 필드 설정 (기본값: true)

#### 완료 확인 (Done)
- [ ] 모든 필수 필드 작성 완료
- [ ] JSON 문법 오류 없음 확인
- [ ] 템플릿의 fields와 capabilities의 field 참조 일치 확인

### 2.3 검증 단계

#### 할 일 (To Do)
- [ ] CLI 명령어 실행: `sdt-validate agent <agent_file.json>`
- [ ] 템플릿 파일과 함께 검증: `sdt-validate agent <agent_file.json> --template <template_file.json>`
- [ ] 검증 오류 수정 (있는 경우)
- [ ] 최종 검증 통과 확인

#### 완료 확인 (Done)
- [ ] 스키마 검증 통과 ("OK" 출력 확인)
- [ ] 템플릿 참조 검증 통과
- [ ] 모든 capabilities의 field 참조 유효성 확인 완료

### 2.4 배포 및 사용 단계

#### 할 일 (To Do)
- [ ] 에이전트 파일을 적절한 위치에 저장
- [ ] 에이전트를 사용할 애플리케이션에 통합
- [ ] 사용자 테스트 및 피드백 수집
- [ ] 필요시 에이전트 수정 및 재검증

#### 완료 확인 (Done)
- [ ] 에이전트 파일 배포 완료
- [ ] 애플리케이션 통합 완료
- [ ] 초기 테스트 완료

## 3. Self-Determination Theory에 맞는 설계 상세 설명

### 3.1 자율성 (Autonomy) 지원 설계

#### 3.1.1 구조적 자율성

에이전트 설계는 사용자에게 **구조를 제공하지만 통제하지 않습니다**:

```json
{
  "capabilities": [
    {
      "type": "capture",
      "field": "reflection",
      "trigger": "manual"  // 사용자가 직접 선택
    }
  ]
}
```

- **Trigger 옵션**: `manual`, `on_field_change`, `on_time_interval`, `on_session_end`, `on_condition_met`
- 사용자는 언제든지 `trigger: "manual"`을 선택하여 완전한 제어권을 가질 수 있습니다.
- `enabled: false`로 설정하면 에이전트를 완전히 비활성화할 수 있습니다.

#### 3.1.2 선택의 자유

- **Capabilities 선택**: 사용자는 필요한 capabilities만 선택하여 에이전트를 구성합니다.
- **SDT 지원 선택**: `sdt_support` 객체에서 어떤 SDT 요소를 강조할지 선택할 수 있습니다.
- **필드 매핑**: 템플릿의 모든 필드를 사용할 필요 없이, 필요한 필드만 capabilities에 매핑합니다.

#### 3.1.3 검증을 통한 자율성 보장

CLI의 검증 프로세스는:

1. **구조 검증**: JSON 스키마를 준수하는지 확인하여 기술적 오류를 방지합니다.
2. **참조 검증**: 템플릿과의 일관성을 확인하여 사용자가 의도한 대로 작동하도록 보장합니다.
3. **강제 없음**: 검증은 "올바른" 사용법을 강제하지 않고, 구조적 일관성만 확인합니다.

### 3.2 유능감 (Competence) 지원 설계

#### 3.2.1 성장 추적 능력

에이전트는 사용자가 정의한 성장을 추적할 수 있도록 설계됩니다:

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
    "competence": "사용자가 정의한 세션 길이의 추세를 분석하여 성장을 시각화합니다."
  }
}
```

- **Analyze Capability**: 사용자 데이터를 분석하여 패턴과 추세를 발견합니다.
- **사용자 정의 메트릭**: 템플릿의 `metrics`와 연계하여 사용자가 정의한 성장 지표를 추적합니다.

#### 3.2.2 즉각적 피드백

- **Suggest Capability**: 사용자의 입력에 따라 즉각적인 제안을 제공합니다.
- **Remind Capability**: 사용자가 설정한 간격으로 성장을 상기시킵니다.

#### 3.2.3 투명한 작동

- **명확한 설명**: `description`과 `sdt_support`를 통해 에이전트가 어떻게 작동하는지 명확히 설명합니다.
- **예측 가능성**: Trigger와 config를 통해 사용자는 에이전트의 작동 시점과 방식을 예측할 수 있습니다.

### 3.3 관계성 (Relatedness) 지원 설계

#### 3.3.1 선택적 공유

```json
{
  "sdt_support": {
    "relatedness": "사용자가 선택적으로 반성(reflection)을 공유할 수 있습니다. 강제되지 않습니다."
  }
}
```

- **Optional 필드**: 템플릿의 `optional: true` 필드를 활용하여 공유를 선택적으로 만듭니다.
- **Manual Trigger**: 공유 관련 capabilities는 `trigger: "manual"`을 사용하여 사용자가 완전한 제어권을 가집니다.

#### 3.3.2 비강제적 연결

- 에이전트는 관계성을 **지원**하지만 **강제하지 않습니다**.
- `sdt_support.relatedness`는 설명일 뿐, 필수 기능이 아닙니다.

### 3.4 통합 설계 원칙

#### 3.4.1 템플릿 기반 일관성

에이전트는 반드시 템플릿을 참조합니다 (`template_id`). 이는:

- **구조적 일관성**: 동일한 템플릿을 사용하는 여러 에이전트 간 일관성 유지
- **확장 가능성**: 템플릿을 수정하면 해당 템플릿을 사용하는 모든 에이전트에 영향을 줄 수 있음
- **검증 가능성**: 템플릿과 에이전트 간 참조를 검증하여 오류 방지

#### 3.4.2 Capabilities의 모듈화

각 capability는 독립적으로 작동하며, 사용자는 필요한 것만 선택할 수 있습니다:

- **Capture**: 데이터 수집
- **Suggest**: 제안 제공
- **Remind**: 알림 제공
- **Analyze**: 분석 수행
- **Custom**: 사용자 정의 기능

#### 3.4.3 검증 프로세스의 SDT 정렬

CLI의 검증 프로세스 자체가 SDT 원칙을 따릅니다:

1. **자율성**: 검증은 "올바른" 사용법을 강제하지 않고, 구조적 일관성만 확인합니다.
2. **유능감**: 검증을 통해 사용자가 의도한 대로 에이전트가 작동할 것임을 보장합니다.
3. **관계성**: 템플릿과의 참조 검증을 통해 다른 구성 요소와의 일관성을 보장합니다.

### 3.5 실제 사용 예시

#### 예시 1: 게임 성장 추적 에이전트

```json
{
  "id": "game-growth-agent-001",
  "name": "게임 세션 분석 에이전트",
  "template_id": "game-growth-basic",
  "description": "플레이어의 게임 세션을 분석하고 성장 추세를 제공합니다.",
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
    "autonomy": "플레이어가 난이도와 세션 길이를 자유롭게 선택합니다.",
    "competence": "세션 길이 추세를 분석하여 플레이어의 지속성 향상을 보여줍니다.",
    "relatedness": "선택적으로 반성을 공유할 수 있습니다."
  },
  "enabled": true
}
```

이 에이전트는:
- **자율성**: 플레이어가 난이도를 선택하고, 반성은 선택 사항입니다.
- **유능감**: 세션 길이 추세 분석을 통해 성장을 보여줍니다.
- **관계성**: 선택적 반성 공유를 지원합니다.

#### 예시 2: 학습 추적 에이전트

```json
{
  "id": "learning-agent-001",
  "name": "학습 진도 알림 에이전트",
  "template_id": "learning-basic",
  "description": "학습자의 진도를 추적하고 주기적으로 알림을 제공합니다.",
  "capabilities": [
    {
      "type": "remind",
      "field": "study_time",
      "trigger": "on_time_interval",
      "config": {
        "interval": "1d",
        "message": "오늘의 학습 시간을 기록해보세요."
      }
    },
    {
      "type": "capture",
      "field": "study_time",
      "trigger": "manual"
    }
  ],
  "sdt_support": {
    "autonomy": "학습자가 언제 학습할지, 얼마나 학습할지 자유롭게 선택합니다.",
    "competence": "학습 시간 추적을 통해 지속적인 학습 습관 형성을 지원합니다.",
    "relatedness": "학습 그룹과 선택적으로 진도를 공유할 수 있습니다."
  },
  "enabled": true
}
```

## 4. CLI 사용법 요약

### 4.1 기본 검증

```bash
sdt-validate agent my_agent.json
```

### 4.2 템플릿과 함께 검증 (권장)

```bash
sdt-validate agent my_agent.json --template my_template.json
```

### 4.3 커스텀 스펙 디렉토리 사용

```bash
sdt-validate agent my_agent.json --spec-dir /path/to/spec
```

### 4.4 검증 성공 시

```
OK
```

### 4.5 검증 실패 시

오류 메시지와 함께 상세한 문제점이 출력됩니다. 이를 수정하고 다시 검증하세요.

## 5. 결론

이 CLI를 사용하여 에이전트를 생성하는 과정은 단순한 기술적 작업이 아닙니다. 그것은 Self-Determination Theory의 원칙에 따라 사용자의 자율성, 유능감, 관계성을 지원하는 도구를 만드는 것입니다. 

검증 프로세스를 통해 구조적 일관성을 보장하면서도, 사용자는 자신의 필요에 맞게 에이전트를 자유롭게 구성하고 수정할 수 있습니다. 이것이 바로 "구조 제공, 통제가 아닌" 설계 철학의 구현입니다.
