
---

## 📁 `diagrams/data_flow.md`

```markdown
```mermaid
sequenceDiagram
    User->>App: Run analysis
    App->>Ingestion: Fetch data
    Ingestion->>Analyzers: Provide inputs
    Analyzers->>App: Metrics
    App->>Report: Save output
