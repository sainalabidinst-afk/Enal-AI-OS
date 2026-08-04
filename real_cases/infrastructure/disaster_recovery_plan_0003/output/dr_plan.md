# Disaster Recovery Plan Output

## DR Strategy
- Strategy: warm_standby
- Primary Region: us-east-1
- Secondary Region: us-west-2

## RPO/RTO Targets
- RPO: 15 minutes
- RTO: 60 minutes

## Backup Schedule
- Frequency: daily
- Retention: 30 days
- Type: full
- Encryption: enabled
- Compression: enabled

## Cost Estimate
- DR infrastructure: 500.00 USD/month
- Backup storage: 20.00 USD/month
- Data transfer: 50.00 USD/month
- Total: 570.00 USD/month

## Compliance
- rpo_within_target: true
- rto_within_target: true
- backup_encrypted: true
- testing_scheduled: true
