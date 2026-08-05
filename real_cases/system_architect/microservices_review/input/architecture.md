# Microservices Architecture Review Case

## Current Architecture

### Service A (User Service)
- Framework: FastAPI
- Database: PostgreSQL
- Responsibilities: User CRUD, Authentication, Profile management

### Service B (Order Service)
- Framework: FastAPI
- Database: PostgreSQL
- Responsibilities: Order processing, Payment integration

### Service C (Notification Service)
- Framework: FastAPI
- Database: Redis
- Responsibilities: Email, SMS, Push notifications

## Issues to Review
1. Service A calls Service B directly (tight coupling)
2. No API Gateway
3. Shared database schema between services
4. No event-driven communication
5. Missing circuit breaker pattern
6. No centralized logging
