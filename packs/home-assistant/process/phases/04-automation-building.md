---
title: 'Phase 4: Automation Building'
type: phase
tags:
- 04-automation-building
- phases
pack: home-assistant-process
retrieval_strategy: atomic
id: home-assistant/process/phases/04-automation-building
verified_at: '2026-04-10'
verified_by: agent
---
# Phase 4: Automation Building

## Goal

Build your first real automations — starting simple, then layering in conditions and templates to make them contextually intelligent. Develop a testing and debugging workflow before your automations grow complex.

## Prerequisites

- Phase 3 complete (devices stable, Areas configured)
- At least one motion sensor, one contact sensor, and some lights
- Familiarity with HA's UI (can navigate Settings, Devices, etc.)

---

## Understanding HA's Automation Model

Every HA automation has three parts:

```
TRIGGER  →  CONDITION  →  ACTION
"When X   if Y is true,   do Z"
happens"
```

**Triggers** fire the automation: motion detected, time reached, state changed, sun rises.  
**Conditions** gate the action: only run if it's after sunset, if someone is home, if the light is already off.  
**Actions** do the work: turn on lights, send notifications, set thermostats, call services.

See Automation Fundamentals for the full model.

---

## Step 1: Your First Automation (UI Method)

Start in the UI, not YAML. The automation editor catches syntax errors and is faster for simple cases.

**Example: Turn on the kitchen light when motion is detected after sunset**

1. Go to **Settings → Automations & Scenes → Create Automation**
2. **Trigger:** Click "Add Trigger" → "Device" → choose your kitchen motion sensor → "Motion detected"
3. **Condition:** Click "Add Condition" → "Sun" → "After sunset" (add offset: 0 minutes)
4. **Action:** Click "Add Action" → "Device" → choose kitchen light → "Turn on"
5. Click "Save" and name it `Kitchen Motion Light — Evening`

**Test it:** Trigger the motion sensor manually (wave at it) after sunset. The light should turn on.

---

## Step 2: Add a Turn-Off Automation

Most people forget the turn-off automation. Lights that turn on automatically should also turn off automatically.

**Example: Turn off kitchen light when no motion for 5 minutes**

The cleanest pattern uses a **timer** or a **delay in the same automation**:

```yaml
# Via UI: use "Wait for trigger" action
- alias: "Kitchen Motion Light — Turn Off"
  trigger:
    - platform: state
      entity_id: binary_sensor.kitchen_motion
      to: "off"
      for:
        minutes: 5
  action:
    - service: light.turn_off
      target:
        entity_id: light.kitchen
```

→ See the full pattern in [[motion-lighting.md|Motion Lighting]]

---

## Step 3: Understand YAML Automations

The UI automation editor generates YAML behind the scenes. Switch to YAML mode by clicking the three-dot menu → "Edit in YAML." This is where you'll spend most of your time once you get comfortable.

**Anatomy of a YAML automation:**

```yaml
- alias: "My Automation Name"          # Required: human-readable name
  description: "What this does"        # Recommended
  mode: single                         # single | restart | queued | parallel
  trigger:
    - platform: state
      entity_id: binary_sensor.front_door
      to: "on"
  condition:
    - condition: state
      entity_id: input_boolean.alarm_armed
      state: "on"
  action:
    - service: notify.mobile_app_my_phone
      data:
        title: "Door Alert"
        message: "Front door opened while alarm is armed"
```

**Automation modes:**
- `single` — if already running, ignore new triggers (default)
- `restart` — cancel and restart on each trigger
- `queued` — queue and run sequentially
- `parallel` — run multiple instances simultaneously

Most automations should be `single` or `restart`.

---

## Step 4: Jinja2 Templates

Templates make automations dynamic — the action changes based on current state. They use Jinja2 syntax inside `{{ }}`.

**Test templates before using them:**

1. Go to **Developer Tools → Template**
2. Type your template and see live output

**Common templates:**

```jinja2
{# Current time as a string #}
{{ now().strftime('%H:%M') }}

{# State of an entity #}
{{ states('sensor.living_room_temperature') }}

{# State converted to float for comparison #}
{{ states('sensor.living_room_temperature') | float(0) }}

{# Friendly name of an entity #}
{{ state_attr('media_player.living_room_tv', 'friendly_name') }}

{# Conditional message #}
{% if states('binary_sensor.front_door') == 'on' %}
  Door is open
{% else %}
  Door is closed
{% endif %}
```

**Using templates in automations:**

```yaml
action:
  - service: notify.mobile_app_my_phone
    data:
      message: >
        Temperature is {{ states('sensor.outside_temperature') }}°F.
        {% if states('sensor.outside_temperature') | float > 85 %}
        Too hot to run.
        {% endif %}
```

---

## Step 5: Helpers — The Glue Layer

**Helpers** are virtual entities you create to hold state used across automations. They're essential for non-trivial logic.

**Common helper types:**

| Helper | Use Case |
|--------|----------|
| `input_boolean` | Toggle switches for modes (vacation mode, sleep mode, guest mode) |
| `input_number` | Adjustable thresholds (motion delay minutes, brightness level) |
| `input_select` | State machines (house mode: Home, Away, Sleep, Guest) |
| `input_datetime` | Adjustable time triggers (wake time, sleep time) |
| `timer` | Countdown timers for motion-off delays |
| `counter` | Track counts (how many times door opened today) |

**Create helpers:** Settings → Devices & Services → Helpers → Add Helper

**Example: House Mode selector controlling many automations:**

```yaml
- alias: "Motion Light — Only When Home"
  trigger:
    - platform: state
      entity_id: binary_sensor.kitchen_motion
      to: "on"
  condition:
    - condition: state
      entity_id: input_select.house_mode
      state: "Home"
  action:
    - service: light.turn_on
      entity_id: light.kitchen
```

---

## Step 6: Testing Workflow

**Always test automations before leaving them running overnight.**

### Quick Testing Tools

1. **Developer Tools → Services:** Manually call any service — trigger fake state changes, test actions
2. **Trace in automation editor:** After an automation runs, open it and click "Traces" to see exactly which path it took and why conditions passed/failed
3. **Developer Tools → States:** Change entity states manually to test conditions
4. **Logbook:** Settings → Logbook shows every state change and automation trigger in order

### Before Committing an Automation

- [ ] Trigger the automation manually at least twice
- [ ] Check the trace to confirm conditions evaluated correctly
- [ ] Test the "off" path (what happens when the trigger condition reverses)
- [ ] Run for 24 hours and check the logbook for unexpected triggers

---

## Step 7: Config Validation

Always validate your configuration after manual YAML edits:

1. **Settings → System → Check Configuration** — validates all YAML files
2. Fix any errors shown before restarting
3. Never restart HA with an invalid configuration — it may fail to start

For add-on YAML (automations, scripts, etc.) edited in the file editor:
```bash
# In Terminal add-on:
ha core check
```

---

## Checklist

- [ ] First motion-triggered automation built and tested
- [ ] Corresponding turn-off automation working
- [ ] House mode helper created (`input_select.house_mode`)
- [ ] At least 3-5 automations running successfully for 48+ hours
- [ ] Template tester used at least once
- [ ] Trace feature understood and used for debugging
- [ ] YAML config checked before every restart
- [ ] Automations organized with clear naming (`Room Action — Condition`)

## What's Next

→ [[05-dashboard-design.md|Phase 5: Dashboard Design]] — Build dashboards for daily at-a-glance control
