# AgentSkills.io Farming Skills

Open source AgentSkills.io format skills for farmers.

---

## Mission

Provide farmers with open source AI skills that automate agricultural operations, support natural farming methods, and enable autonomous farm management.

---

## About AgentSkills.io

AgentSkills is a skill format for autonomous AI assistants. Skills extend AI capabilities with specialized knowledge, tools, and behaviors for specific domains.

---

## Skill Directory Structure

Each skill is a self-contained directory with all necessary files:

```
skill-name/
├── SKILL.md              # Skill definition and instructions
├── tools.json            # Tool configurations (optional)
├── .env.example          # Environment variables template for credentials
├── scripts/              # Helper scripts and utilities
├── examples/             # Example outputs and use cases
├── references/           # Documentation and reference materials
└── resources/           # Templates, configs, data files
```

---

## SKILL.md Format

Each skill must include a `SKILL.md` file that follows this structure:

```markdown
# Skill Name

Brief description of what this skill does.

## Purpose

Detailed explanation of skill's purpose and goals.

## Capabilities

List of specific capabilities and use cases.

## Instructions

How the AI agent should use this skill.

## Tools

Any tools this skill uses or requires.

## Environment Variables

Required credentials or configuration (see .env.example).

## Examples

Example usage scenarios.

## References

Links to documentation, research, or external resources.
```

---

## .env.example Format

Each skill should include a `.env.example` file that documents required credentials and configuration:

```bash
# Weather API Key (optional - uses wttr.in by default)
WEATHER_API_KEY=your_api_key_here

# Soil database API (optional)
SOIL_DB_API_KEY=your_api_key_here

# Local configuration
SKILL_DEBUG=false
SKILL_LOG_LEVEL=info
```

Usage:
```bash
# Copy example to create actual .env file
cp .env.example .env

# Edit with your credentials
nano .env

# .env is in .gitignore - never commit actual credentials
```

---

## tools.json Format

Optional JSON file defining tool configurations:

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "tools": [
    {
      "name": "check_weather",
      "description": "Check current weather conditions",
      "command": "weather-check",
      "params": ["location", "units"]
    }
  ],
  "dependencies": [
    {"name": "curl", "required": true},
    {"name": "jq", "required": false}
  ]
}
```

---

## Skill Categories

This repository contains skills for the following agricultural domains:

- **Weather Monitoring** - Real-time weather tracking, freeze alerts, thaw windows
- **Farm Rehabilitation** - Post-freeze damage assessment and recovery
- **JADAM Natural Farming** - Ferment-based inputs, JWA, JLF, JLF+, WCA
- **Worm Farming** - Bin setup, feeding, health monitoring, harvesting
- **Ferments & Inputs** - Recipes, protocols, temperature tracking, batch logs
- **Crop Management** - Planting schedules, growth tracking, health monitoring
- **IoT & Sensors** - Sensor deployment, data collection, automated alerts
- **Documentation** - Daily logs, reports, seasonal planning

---

## Installation

### Clone Repository

```bash
git clone https://github.com/farmfriend-labs/agent-skills-farming.git
cd agent-skills-farming
```

### Use with FF-Terminal

```bash
# Copy skill to FF-Terminal skills directory
cp -r skills/weather-monitoring ~/.ff-terminal/skills/

# Load skill via FF-Terminal
ff-terminal --load-skill weather-monitoring
```

### Use with Other Agents

Skills use standard AgentSkills.io format and work with compatible agents:

```bash
# Load skill into agent context
agent --skill ./skills/weather-monitoring

# Or copy to agent skills directory
cp -r skills/weather-monitoring ~/.agent/skills/
```

---

## Development Guidelines

### Creating a New Skill

1. Create directory: `skills/your-skill-name/`
2. Create `SKILL.md` with proper format
3. Add `.env.example` for any credentials needed
4. Create `scripts/` for any helper utilities
5. Add `examples/` with usage scenarios
6. Document `references/` with supporting materials
7. Add skill to this README under appropriate category

### Skill Requirements

- **SKILL.md**: Required - defines skill behavior
- **.env.example**: Required if skill uses credentials/APIs
- **scripts/**: Optional - helper scripts
- **examples/**: Optional - usage examples
- **references/**: Optional - documentation
- **resources/**: Optional - templates, configs

### Environment Variables

- Use `.env.example` to document required variables
- Add `.env` to `.gitignore` (never commit credentials)
- Provide clear instructions in SKILL.md for setup

---

## Contributing

We welcome contributions! To add a skill:

1. Fork this repository
2. Create a new skill directory following the structure above
3. Add skill to README under appropriate category
4. Submit a pull request

Guidelines:
- Skills must work offline whenever possible
- Use plain language, no jargon
- Include clear setup instructions
- Document all environment variables
- Provide working examples

---

## License

MIT License - Open source, free to use, modify, and distribute.

### What This Means

- Use skills for personal or commercial farming
- Modify skills for your specific needs
- Distribute modified versions
- Include attribution to original authors
- No warranty, use at your own risk

---

## Support

### Documentation

See [FF-Docs](https://github.com/farmfriend-labs/ff-docs) for detailed guides and tutorials (coming soon).

### Community

Join the discussion in [Issues](https://github.com/farmfriend-labs/agent-skills-farming/issues) or [Discussions](https://github.com/farmfriend-labs/agent-skills-farming/discussions).

### Contact

- Email: farmfriend.labs@gmail.com
- Website: https://farm-friend.com
- Location: Cedar Creek, TX

---

## Related Projects

- [FF-Terminal](https://github.com/farmfriend-labs/ff-terminal) - Autonomous AI terminal (coming soon)
- [FF-Agriculture](https://github.com/farmfriend-labs/ff-agriculture) - Farm automation platform (planned)
- [FF-JADAM](https://github.com/farmfriend-labs/ff-jadam) - JADAM natural farming implementation (planned)

---

## Acknowledgments

- JADAM methods from Youngsang Cho and JADAM Global
- AgentSkills.io format specification
- FarmFriend Terminal Labs community contributors
- Open source agricultural technology community

---

FarmFriend Terminal Labs - Open Source Skills for Farmers
