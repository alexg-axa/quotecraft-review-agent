# QuoteCraft Architecture Review Findings

## Executive Summary

- QuoteCraft is not fully compliant with Silver tier requirements for availability, security, and cost management as defined by AlphaPaaS standards.
- Critical security gaps exist, including use of long-lived IAM keys, plaintext Redis traffic, and certificate verification disabled for a third-party integration.
- The deployment and infrastructure do not meet Silver tier requirements for multi-AZ, autoscaling, and resource right-sizing.
- Cost inefficiencies are present, notably in non-production environment spend and over-provisioned EFS throughput.
- Several issues are already tracked in the backlog but remain unremediated.

## Findings

### Cost

#### F-01: Non-production environment exceeds cost threshold
- Severity: Critical
- Dimension: Cost
- Evidence:
  - Source: case:hackathon-assets/hackathon-quotecraft-intake-form.pdf
  - Quote: "The FinOps team flagged in March 2026 that QuoteCraft's non-production environment is consuming approximately 35% of what production consumes. The cause has not been investigated."
- Policy reference: FIN-07
- Why it matters: Non-production spend must not exceed 20% of production spend. Overspending reduces available budget and triggers FinOps review.
- Remediation: Investigate non-production environment resource usage and downsize or schedule off workloads to bring spend below 20% of production.
- Confidence: High

#### F-02: Over-provisioned EFS throughput
- Severity: High
- Dimension: Cost
- Evidence:
  - Source: app:infra/aws/efs.tf
  - Quote: "Provisioned throughput. Originally set during the pilot when we thought PDF generation would be I/O bound. It isn't. Tracked in QC-211."
- Policy reference: FIN-06
- Why it matters: Provisioned throughput storage must only be used when required. Over-provisioning increases monthly costs unnecessarily.
- Remediation: Revert EFS to bursting throughput mode unless a documented IOPS requirement justifies provisioned mode.
- Confidence: High

#### F-03: S3 archive storage lacks lifecycle policy
- Severity: Medium
- Dimension: Cost
- Evidence:
  - Source: app:infra/aws/s3.tf
  - Quote: "# NB: No lifecycle configuration. Quote archives are kept in STANDARD storage class indefinitely. There was a ticket to add glacier transition (QC-134) but it was deprioritised."
- Policy reference: FIN-13
- Why it matters: Without lifecycle policies, long-term archives remain in expensive storage, increasing costs over time.
- Remediation: Implement S3 lifecycle policy to transition quote archives to Glacier or equivalent after 30 days.
- Confidence: High

#### F-04: Application logs retained longer than required
- Severity: Low
- Dimension: Cost
- Evidence:
  - Source: app:infra/aws/cloudwatch.tf
  - Quote: "retention_in_days = 365" for application logs
- Policy reference: FIN-16
- Why it matters: Silver tier requires 90-day retention for application logs; longer retention increases storage costs.
- Remediation: Reduce application log retention to 90 days for Silver tier workloads.
- Confidence: High

### Security

#### F-05: Long-lived IAM user access keys in use
- Severity: Critical
- Dimension: Security
- Evidence:
  - Source: app:deploy/openshift/secret-aws-keys.yaml
  - Quote: "# Long-lived IAM user access keys for reading from AWS Secrets Manager and mounting EFS. Created by the initial platform onboarding. There's a ticket to migrate to IRSA (QC-203) but it's not scheduled yet."
- Policy reference: CKS-06, ASC-06, AHS-11
- Why it matters: Long-lived credentials are prohibited; workload identity federation is required to reduce risk of credential compromise.
- Remediation: Migrate to IRSA (IAM Roles for Service Accounts) for AWS access and remove long-lived IAM user keys.
- Confidence: High

#### F-06: Redis traffic is unencrypted and uses plaintext protocol
- Severity: Critical
- Dimension: Security
- Evidence:
  - Source: app:infra/aws/elasticache.tf
  - Quote: "transit_encryption_enabled = false ... NB: TLS in transit is not enabled. Enabling it would require an application change (rediss:// URL and CA bundle). Tracked in QC-176."
  - Source: app:src/quotecraft/cache.py
  - Quote: "# NB: redis:// (not rediss://). ElastiCache was provisioned without transit_encryption_enabled to simplify the initial migration from the in-process cache."
- Policy reference: ASC-03, ASC-04, DCH-04
- Why it matters: Redis traffic includes PII and must be encrypted in transit. Plaintext traffic exposes sensitive data to interception.
- Remediation: Enable TLS for ElastiCache and update application to use rediss:// with CA bundle.
- Confidence: High

#### F-07: Certificate verification disabled for third-party API
- Severity: High
- Dimension: Security
- Evidence:
  - Source: app:src/quotecraft/integrations/bureau.py
  - Quote: "# NB: verify=False — see module docstring. TODO(QC-189): migrate to verify=True once the Atlas production CA is added to the base image trust store."
- Policy reference: DCH-05
- Why it matters: Disabling certificate verification allows MITM attacks, risking exposure of Restricted data.
- Remediation: Add the Atlas CA to the trust store and set verify=True for requests to the bureau API.
- Confidence: High

#### F-08: Broad RBAC permissions granted to operator ServiceAccount
- Severity: High
- Dimension: Security
- Evidence:
  - Source: app:deploy/openshift/rbac.yaml
  - Quote: "rules: ... apiGroups: [\"*\"], resources: [\"*\"], verbs: [\"*\"] ... In practice the operator only reads ConfigMaps and updates its own status, but this Role was copied from an earlier internal tool and never tightened."
- Policy reference: CKS-14
- Why it matters: Wildcard RBAC permissions increase blast radius in case of compromise and violate least privilege.
- Remediation: Restrict Role to only required resources and verbs (e.g., ConfigMaps, status updates).
- Confidence: High

#### F-09: Secrets injected as environment variables
- Severity: Medium
- Dimension: Security
- Evidence:
  - Source: app:deploy/openshift/deployment.yaml
  - Quote: "envFrom: ... secretRef: ... name: quotecraft-secrets"
- Policy reference: CKS-11, DCH-07
- Why it matters: Secrets in environment variables can be exposed via logs, process listings, or crash dumps.
- Remediation: Refactor deployment to mount secrets as files using CSI driver or External Secrets Operator.
- Confidence: High

#### F-10: Postgres connection does not verify server certificate
- Severity: Medium
- Dimension: Security
- Evidence:
  - Source: app:src/quotecraft/config.py
  - Quote: "# NB: sslmode=require (not verify-full). Connection is encrypted but the server certificate is not validated against a CA. This was inherited from a staging config and was never revisited."
- Policy reference: DCH-05
- Why it matters: Without certificate verification, connections are vulnerable to MITM attacks.
- Remediation: Update Postgres DSN to use sslmode=verify-full and ensure CA bundle is available.
- Confidence: High

### Scalability

#### F-11: In-memory rate limiter not safe for multi-replica deployments
- Severity: High
- Dimension: Scalability
- Evidence:
  - Source: app:src/quotecraft/middleware/rate_limit.py
  - Quote: "This is the same implementation we've used since pilot. It works well for single-replica deployments; horizontal scaling will be addressed in QC-201."
  - Source: app:docs/runbook.md
  - Quote: "This is a known issue with the current in-memory rate limiter when the service is scaled to multiple pods — each pod enforces the limit independently."
- Policy reference: ARS-14
- Why it matters: Rate limiting is not enforced correctly when scaled horizontally, risking abuse or denial of service.
- Remediation: Externalize rate limiter state to Redis or another shared store to support correct enforcement across replicas.
- Confidence: High

#### F-12: Database connection pool not implemented
- Severity: Medium
- Dimension: Scalability
- Evidence:
  - Source: app:src/quotecraft/db.py
  - Quote: "# TODO(QC-142): migrate to psycopg_pool.ConnectionPool once we address the connection storm issue reported in INC-44231. For now we open a connection per request; at low baseline traffic this is acceptable, but the capacity plan anticipates 400 req/s at peak which we have not yet stress-tested."
- Policy reference: ARS-06
- Why it matters: Lack of connection pooling may cause connection storms and degrade performance under load.
- Remediation: Implement a shared connection pool for Postgres connections.
- Confidence: High

### Availability

#### F-13: Deployment does not meet Silver tier multi-AZ and replica requirements
- Severity: Critical
- Dimension: Availability
- Evidence:
  - Source: app:deploy/openshift/deployment.yaml
  - Quote: "replicas: 1 ... nodeSelector: failure-domain.alphapaas.com/zone: \"1\""
  - Source: app:docs/architecture.md
  - Quote: "QuoteCraft runs as three pairs of pods distributed across the three availability zones ... HPA adjusts replica count between 6 and 30 ... Pod placement is managed by topology spread constraints"
  - Source: app:docs/capacity-plan.md
  - Quote: "Expected baseline replica count: 6 (2 per AZ) ... Open items: ... Zone-redundant HA for Postgres (QC-193) ... Multi-AZ ElastiCache replication (QC-177)"
- Policy reference: ARS-02, ARS-05, ARS-18
- Why it matters: Silver tier requires at least 3 replicas, multi-AZ distribution, and zone-redundant data stores. Current deployment manifest specifies only 1 replica in a single zone.
- Remediation: Update deployment to use at least 3 replicas with topology spread constraints across AZs; ensure managed services are zone-redundant.
- Confidence: High

#### F-14: ElastiCache and Postgres not zone-redundant
- Severity: High
- Dimension: Availability
- Evidence:
  - Source: app:infra/aws/elasticache.tf
  - Quote: "num_cache_nodes = 1 ... availability_zone = \"${var.aws_region}a\""
  - Source: app:infra/azure/postgres.tf
  - Quote: "# Zone-redundant HA is not configured. ... Public access enabled for developer convenience during the initial roll-out. There is a ticket to lock this down (QC-193) but it has not been scheduled."
  - Source: app:docs/capacity-plan.md
  - Quote: "Open items: ... Zone-redundant HA for Postgres (QC-193) ... Multi-AZ ElastiCache replication (QC-177)"
- Policy reference: ARS-18, ASC-03
- Why it matters: Single-AZ managed services are a single point of failure and do not meet Silver tier requirements.
- Remediation: Enable zone-redundant HA for Postgres and deploy ElastiCache as a replication group across at least two AZs.
- Confidence: High

#### F-15: No documented or tested DR exercise
- Severity: Medium
- Dimension: Availability
- Evidence:
  - Source: app:docs/capacity-plan.md
  - Quote: "DR exercise: **not yet performed.** Scheduled for Q3 2026."
- Policy reference: ARS-20
- Why it matters: Silver tier workloads must undergo a documented DR exercise at least once every twelve months.
- Remediation: Schedule and execute a DR exercise simulating AZ loss and document the outcome.
- Confidence: High

#### F-16: Use of deprecated DeploymentConfig for worker
- Severity: Low
- Dimension: Availability
- Evidence:
  - Source: app:deploy/openshift/worker-deploymentconfig.yaml
  - Quote: "kind: DeploymentConfig ... The legacy DeploymentConfig resource MUST NOT be used for new deployments, and existing usage MUST be migrated at the next major release of the application."
- Policy reference: ARS-03, ARS-23
- Why it matters: DeploymentConfig is deprecated and must be migrated to Deployment for Silver tier workloads.
- Remediation: Migrate worker deployment to use apps/v1 Deployment resource.
- Confidence: High

## Highest Priority Next Actions

1. Migrate from long-lived IAM user keys to workload identity federation (IRSA) for AWS access (Critical Security).
2. Enable TLS for ElastiCache Redis and update application to use encrypted connections (Critical Security).
3. Update deployment to meet Silver tier: at least 3 replicas, topology spread constraints, and zone-redundant managed services (Critical Availability).
4. Investigate and reduce non-production environment spend to below 20% of production (Critical Cost).
5. Add certificate verification for all outbound HTTPS connections, especially the Atlas Credit Bureau API (High Security).

## Report Quality Check

- Findings are grouped by Cost, Security, Scalability, Availability. **Pass**
- Every finding cites at least one evidence source. **Pass**
- Every finding cites at least one policy clause. **Pass**
- Findings are specific to QuoteCraft, not generic cloud advice. **Pass**
- Recommendations are concrete enough for backlog tickets. **Pass**