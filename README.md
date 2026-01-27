# AgentSkills.io Farming Skills

Open source AgentSkills.io format skills for farmers. Comprehensive collection of agricultural skills for autonomous AI assistants, covering farm rehabilitation, JADAM natural farming, worm farming, ferments, weather monitoring, and agricultural technology development.

---

## Mission

Provide farmers with open source AI skills that automate agricultural operations, support natural farming methods, and enable autonomous farm management.

---

## About AgentSkills.io

AgentSkills is a skill format for autonomous AI assistants. Skills extend AI capabilities with specialized knowledge, tools, and behaviors for specific domains.

**Skill Structure:**
```
skill-name/
├── SKILL.md              # Skill definition and instructions
├── tools.json            # Tool configurations (optional)
├── examples/             # Example outputs and use cases
└── references/          # Documentation and reference materials
```

---

## Available Skills

### Weather Monitoring
- **skill/weather-monitoring** - Real-time weather tracking, freeze alerts, thaw windows
- **skill/weather-forecast** - Multi-day forecasting for planning
- **skill/weather-automation** - Automated alerts for critical conditions

### Farm Rehabilitation
- **skill/farm-rehab** - Post-freeze damage assessment and recovery
- **skill/infrastructure-inspection** - Pipe, equipment, and building checks
- **skill/soil-health** - Soil analysis and remediation tracking

### JADAM Natural Farming
- **skill/jadam-intro** - Introduction to JADAM methods
- **skill/jadam-ferments** - Ferment-based inputs (JWA, JLF, JLF+) recipes
- **skill/jadam-wca** - Water-Capped Aerobics for inputs
- **skill/jadam-sea-solution** - Sea water-based nutrient solutions

### Worm Farming
- **skill/worm-bin-setup** - Bin construction and population
- **skill/worm-feeding** - Feeding schedules and materials
- **skill/worm-harvest** - Casting collection and processing
- **skill/worm-health** - Temperature, moisture, and activity monitoring

### Ferments & Inputs
- **skill/ferment-recipe** - Input recipes and protocols
- **skill/ferment-temperature** - Temperature monitoring and control
- **skill/ferment-tracking** - Batch logs and quality tracking
- **skill/input-scheduling** - Input application timing and rates

### Crop Management
- **skill/crop-planting** - Schedules and best practices
- **skill/crop-monitoring** - Growth stage tracking
- **skill/crop-health** - Disease and pest detection
- **skill/harvest-timing** - Optimal harvest windows

### IoT & Sensors
- **skill/sensor-setup** - Temperature, moisture, pH sensor deployment
- **skill/sensor-data** - Data collection and storage
- **skill/sensor-alerts** - Automated threshold notifications

### Documentation
- **skill/farm-logging** - Daily operation logs
- **skill/farm-reports** - Weekly/monthly summaries
- **skill/farm-planning** - Seasonal goals and milestones

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
cp -r skill/weather-monitoring ~/.ff-terminal/skills/

# Load skill via FF-Terminal
ff-terminal --load-skill weather-monitoring
```

### Use with Other Agents

Skills use standard AgentSkills.io format and work with compatible agents:

```bash
# Load skill into agent context
agent --skill ./skill/weather-monitoring

# Or copy to agent skills directory
cp -r skill/weather-monitoring ~/.agent/skills/
```

---

## Usage Examples

### Weather Freeze Alert

```
User: Check for freeze conditions tonight.

Agent: [Using weather-monitoring skill]
Current temp: 28°F
Tonight's low: 22°F
Freeze alert in effect.
Recommended actions:
- Protect ferments
- Insulate worm bins
- Cover sensitive crops
```

### JADAM Ferment Recipe

```
User: Help me create a JWA ferment.

Agent: [Using jadam-ferments skill]
JWA (JADAM Water-soluble Amino acid) Recipe:

Ingredients:
- 100 kg waste fish (ground)
- 10 kg brown sugar
- 100 L water
- 2 kg effective microorganisms (EM)

Instructions:
1. Mix fish and sugar in container
2. Add water, stir thoroughly
3. Add EM culture
4. Seal with airlock
5. Ferment 5-7 days at 25-30°C
6. Strain liquid, store in airtight container

Usage: Dilute 1:500 for foliar spray
```

### Worm Bin Health Check

```
User: Check worm bin conditions.

Agent: [Using worm-health skill]
Bin Status:
- Temperature: 68°F (optimal)
- Moisture: 75% (optimal)
- Activity: High
- Bedding: Needs refresh

Recommendations:
- Add fresh bedding material
- Monitor feeding rate
- No action needed on temperature/moisture
```

---

## Skill Structure

### SKILL.md Format

```markdown
# Skill Name

Brief description of what this skill does.

## Purpose

Detailed explanation of the skill's purpose and goals.

## Capabilities

List of specific capabilities and use cases.

## Instructions

How the agent should use this skill.

## Tools

Any tools this skill uses or requires.

## Examples

Example usage scenarios.
```

### tools.json Format

```json
{
  "tools": [
    {
      "name": "weather_check",
      "description": "Check current weather conditions",
      "parameters": {
        "location": "string (optional)",
        "units": "string (celsius/fahrenheit)"
      }
    }
  ]
}
```

---

## Development

### Creating New Skills

1. Create skill directory: `skill/my-new-skill/`
2. Add `SKILL.md` with skill definition
3. Add `tools.json` if needed
4. Add examples in `examples/` directory
5. Submit pull request

### Skill Guidelines

- Purpose-focused: Each skill solves a specific farming problem
- Practical: Real-world use cases, not theoretical
- Documented: Clear instructions and examples
- Tested: Verify skills work with FF-Terminal
- Sustainable: Align with natural farming principles

---

## Contributing

We welcome contributions from farmers, AI researchers, and agricultural technologists.

### How to Contribute

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-skill`
3. Add your skill following skill structure
4. Test with FF-Terminal or compatible agent
5. Submit pull request with description

### Contribution Areas

- New farming skills
- Improved documentation
- Example use cases
- Bug fixes
- Performance optimizations
- Translations (multi-language support)

---

## Roadmap

### Phase 1: Core Skills (Q1 2026)
- [x] Weather monitoring
- [x] Farm rehabilitation
- [x] JADAM basic skills
- [ ] Worm farming complete
- [ ] Ferment tracking

### Phase 2: Expansion (Q2 2026)
- [ ] Crop management
- [ ] IoT sensor integration
- [ ] Automated alerts
- [ ] Data visualization
- [ ] Mobile compatibility

### Phase 3: AI Enhancement (Q3 2026)
- [ ] Predictive analytics
- [ ] Decision support
- [ ] Anomaly detection
- [ ] Multi-farm coordination
- [ ] Resource optimization

### Phase 4: Ecosystem (Q4 2026)
- [ ] Community marketplace
- [ ] Skill validation system
- [ ] Contribution rewards
- [ ] Partner integrations
- [ ] Regional adaptations

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

See [FF-Docs](https://github.com/farmfriend-labs/ff-docs) for detailed guides and tutorials.

### Community

Join the discussion in [Issues](https://github.com/farmfriend-labs/agent-skills-farming/issues) or [Discussions](https://github.com/farmfriend-labs/agent-skills-farming/discussions).

### Contact

- Email: farmfriend.labs@gmail.com
- Website: https://farm-friend.com
- Location: Cedar Creek, TX

---

## Related Projects

- [FF-Terminal](https://github.com/farmfriend-labs/ff-terminal) - Autonomous AI terminal
- [FF-Agriculture](https://github.com/farmfriend-labs/ff-agriculture) - Farm automation platform
- [FF-JADAM](https://github.com/farmfriend-labs/ff-jadam) - JADAM natural farming implementation

---

## Acknowledgments

- JADAM methods from Youngsang Cho and JADAM Global
- AgentSkills.io format specification
- FarmFriend Terminal Labs community contributors
- Open source agricultural technology community

---

FarmFriend Terminal Labs - Open Source Skills for Farmers
