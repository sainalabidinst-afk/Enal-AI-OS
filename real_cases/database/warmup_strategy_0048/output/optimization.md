# warmup_strategy - Database Optimization

## Schema Review
- Missing indexes on foreign keys
- No partitioning strategy
- Missing check constraints

## Query Optimization
- Add composite index on orders(user_id, status)
- Consider partitioning orders by created_at
- Add covering index for common queries

## Recommendations
1. Add indexes: user_id, created_at
2. Implement partitioning for large tables
3. Add check constraints for data integrity
4. Consider read replicas for reporting
