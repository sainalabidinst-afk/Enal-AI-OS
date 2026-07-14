# RFC Process

This document describes the Request for Comments (RFC) process for ECP.

## Purpose

The RFC process ensures that significant changes to ECP are well-designed, reviewed, and documented before implementation.

## When to Write an RFC

Write an RFC for:
- New features or major functionality
- Changes to existing contracts/APIs
- Architectural changes
- Breaking changes
- New plugins or tools that affect core behavior

## RFC Template

```markdown
# RFC-XXXX: Title

## Summary
One-paragraph summary of the proposal.

## Motivation
Why should we do this? What problem does it solve?

## Detailed Design
Technical details of the proposal.

## Alternatives Considered
What other approaches were considered?

## Compatibility
How does this affect backward compatibility?

## Security Considerations
Any security implications?

## Testing Strategy
How will this be tested?

## Timeline
Proposed timeline for implementation.

## References
Related RFCs, documentation, etc.
```

## RFC Process

1. **Draft**: Author creates RFC in `docs/rfcs/`
2. **Review**: Community reviews for 7 days
3. **Revision**: Author addresses feedback
4. **Acceptance**: Core team accepts or rejects
5. **Implementation**: Author implements with guidance
6. **Integration**: Merged into main branch

## Current RFCs

- RFC-0001: Stable Contracts (Accepted)
- RFC-0002: Plugin Manifest Format (Accepted)
- RFC-0003: SDK Decorators (Accepted)
