# RFC: Code Knowledge Expansion

**Status:** Planned
**Target:** Capability Excellence phase
**Capability Pack:** Code Engineer

## Summary

Expand Code Engineer knowledge depth across software design principles, architecture patterns, and secure coding practices.

## Knowledge Domains

### Clean Architecture
- Layers: entities, use cases, interface adapters, frameworks
- Dependency rule
- Boundaries and interfaces
- Testing isolation through architecture
- When to apply vs over-engineering

### DDD (Domain-Driven Design)
- Bounded contexts
- Entities, Value Objects, Aggregates
- Domain events
- Repository and specification patterns
- Anti-corruption layers
- Ubiquitous language

### SOLID
- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion
- Practical examples in Python/TypeScript

### CQRS
- Command vs Query separation
- Write model and read model
- Event sourcing integration
- Consistency models
- When to use CQRS

### Event Sourcing
- Event store concepts
- Event schema design
- Replay and projection
- Snapshotting
- Integration with CQRS

### Secure Coding
- OWASP Top 10 mapping
- Injection prevention
- Authentication and authorization patterns
- Secrets management
- Secure dependency handling

## Implementation Approach

All knowledge is added to the Code Capability Pack domain engine. No Core changes are required.

## Success Criteria

- Each knowledge domain is represented in code generation, review, and refactoring logic
- Golden tests cover new patterns
- Benchmark scores for code quality and explainability improve

## References

- RFC-0006: Code Knowledge Base
- CAPABILITY_GUIDE.md — Code Engineer section
