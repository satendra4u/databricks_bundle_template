# Governance for {{.project_name}}

## Ownership
- Product Owner: <owner@company.com>
- Tech Lead: <techlead@company.com>
- Data Steward: <steward@company.com>

## Environments
- Dev: adhoc development and testing
- Prod: controlled deployments through CI/CD

## Processes
- Code changes via PR with at least one reviewer.
- CI runs lint and validations; deployments gated on CI success.
- Models must be registered to Unity Catalog with proper approval.

## Data Policy
- Use Unity Catalog-managed tables for all curated data.
- PII handling must follow company policy.

## Access Control
- Jobs run with least privilege.
- Cluster and Serving policies are defined in `policies/`.
