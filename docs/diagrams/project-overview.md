# Project Overview & Architecture

## 🏗️ Complete System Architecture

```mermaid
graph TB
    subgraph "User Interface"
        A[User Input] --> B[Command Line]
        B --> C[Configuration]
    end
    
    subgraph "Core Pipeline"
        D[TrendAgent] --> E[IdeaAgent]
        E --> F[HookAgent]
        F --> G[DraftingAgent]
        G --> H[ComplianceAgent]
        H --> I[PersonaAgent]
        I --> J[PeerReviewAgent]
        J --> K[EngagementAgent]
    end
    
    subgraph "External Services"
        L[Google Gemini API]
        M[Twitter API v2]
        N[OAuth2 Authentication]
    end
    
    subgraph "Data Storage"
        O[SQLite Database]
        P[Log Files]
        Q[Configuration Files]
    end
    
    subgraph "Output & Monitoring"
        R[Posted Tweets]
        S[Engagement Analytics]
        T[Performance Metrics]
    end
    
    %% Connections
    A --> D
    C --> D
    E -.-> L
    F -.-> L
    G -.-> L
    I -.-> L
    J -.-> L
    
    J --> M
    K --> M
    M --> N
    
    D --> O
    E --> O
    F --> O
    G --> O
    H --> O
    I --> O
    J --> O
    K --> O
    
    C --> Q
    M --> P
    L --> P
    
    M --> R
    R --> S
    S --> T
    
    style A fill:#e3f2fd
    style B fill:#e3f2fd
    style C fill:#e3f2fd
    style D fill:#e1f5fe
    style E fill:#e1f5fe
    style F fill:#e1f5fe
    style G fill:#f3e5f5
    style H fill:#f3e5f5
    style I fill:#f3e5f5
    style J fill:#e8f5e8
    style K fill:#e8f5e8
    style L fill:#fff3e0
    style M fill:#fff3e0
    style N fill:#fff3e0
    style O fill:#fce4ec
    style P fill:#fce4ec
    style Q fill:#fce4ec
    style R fill:#e8f5e8
    style S fill:#e8f5e8
    style T fill:#e8f5e8
```

## 🔄 Complete Workflow

```mermaid
flowchart TD
    Start([Start Pipeline]) --> Config{Configuration Valid?}
    Config -->|No| Error[Show Error & Exit]
    Config -->|Yes| Trend[TrendAgent: Select Topic]
    
    Trend --> Idea{IdeaAgent: Generate Ideas}
    Idea -->|Success| Hook[HookAgent: Create Hook]
    Idea -->|Failure| Fallback[Use Fallback Topic]
    Fallback --> Hook
    
    Hook -->|Success| Draft[DraftingAgent: Write Content]
    Hook -->|Failure| Idea
    Draft -->|Success| Comply[ComplianceAgent: Check Safety]
    Draft -->|Failure| Hook
    
    Comply -->|Passed| Persona[PersonaAgent: Apply Styling]
    Comply -->|Failed| Draft
    
    Persona -->|Success| Review[PeerReviewAgent: Quality Check]
    Persona -->|Failure| Draft
    Review -->|Approved| Preview[Show Preview]
    Review -->|Rejected| Draft
    
    Preview --> DryRun{DRY_RUN Mode?}
    DryRun -->|Yes| Log[Log to Database]
    DryRun -->|No| Approve{User Approves?}
    
    Approve -->|Yes| Post[Post to Twitter]
    Approve -->|No| Log
    
    Post -->|Success| Monitor[EngagementAgent: Track Performance]
    Post -->|Failure| Error
    
    Monitor --> Log
    Log --> End([Pipeline Complete])
    Error --> End
    
    style Start fill:#e8f5e8
    style End fill:#e8f5e8
    style Error fill:#ffebee
    style Post fill:#e8f5e8
    style Monitor fill:#e8f5e8
```

## 📊 Data Flow Architecture

```mermaid
graph LR
    subgraph "Input Sources"
        A[Trending Topics]
        B[User Preferences]
        C[Brand Guidelines]
        D[API Keys]
    end
    
    subgraph "Processing Engine"
        E[LLM Generation]
        F[Content Validation]
        G[Style Application]
        H[Quality Assurance]
    end
    
    subgraph "Storage Layer"
        I[SQLite Database]
        J[Log Files]
        K[Configuration]
    end
    
    subgraph "Output Destinations"
        L[Twitter Posts]
        M[Analytics Dashboard]
        N[Performance Reports]
    end
    
    A --> E
    B --> E
    C --> E
    D --> E
    
    E --> F
    F --> G
    G --> H
    
    E --> I
    F --> I
    G --> I
    H --> I
    
    E --> J
    F --> J
    G --> J
    H --> J
    
    B --> K
    C --> K
    D --> K
    
    H --> L
    L --> M
    M --> N
    
    style A fill:#e3f2fd
    style B fill:#e3f2fd
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style E fill:#f3e5f5
    style F fill:#f3e5f5
    style G fill:#f3e5f5
    style H fill:#f3e5f5
    style I fill:#fff3e0
    style J fill:#fff3e0
    style K fill:#fff3e0
    style L fill:#e8f5e8
    style M fill:#e8f5e8
    style N fill:#e8f5e8
```

## 🎯 Agent Interaction Matrix

```mermaid
graph TD
    subgraph "Agent Dependencies"
        A[TrendAgent] --> B[IdeaAgent]
        B --> C[HookAgent]
        C --> D[DraftingAgent]
        D --> E[ComplianceAgent]
        E --> F[PersonaAgent]
        F --> G[PeerReviewAgent]
        G --> H[EngagementAgent]
    end
    
    subgraph "External Dependencies"
        I[LLM Router]
        J[Twitter API]
        K[Database]
    end
    
    B -.-> I
    C -.-> I
    D -.-> I
    F -.-> I
    G -.-> I
    
    G --> J
    H --> J
    
    A --> K
    B --> K
    C --> K
    D --> K
    E --> K
    F --> K
    G --> K
    H --> K
    
    style A fill:#e1f5fe
    style B fill:#e1f5fe
    style C fill:#e1f5fe
    style D fill:#f3e5f5
    style E fill:#f3e5f5
    style F fill:#f3e5f5
    style G fill:#e8f5e8
    style H fill:#e8f5e8
    style I fill:#fff3e0
    style J fill:#fff3e0
    style K fill:#fce4ec
```

## 🔧 Configuration Architecture

```mermaid
graph TB
    subgraph "Environment Configuration"
        A[.env File]
        B[Environment Variables]
        C[App Config]
    end
    
    subgraph "API Configuration"
        D[Twitter OAuth2]
        E[Gemini API]
        F[Rate Limits]
    end
    
    subgraph "System Configuration"
        G[DRY_RUN Mode]
        H[Scheduling]
        I[Logging]
        J[Database]
    end
    
    subgraph "Content Configuration"
        K[Content Styles]
        L[Brand Guidelines]
        M[Strictness Levels]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E
    C --> F
    C --> G
    C --> H
    C --> I
    C --> J
    C --> K
    C --> L
    C --> M
    
    style A fill:#e3f2fd
    style B fill:#e3f2fd
    style C fill:#e3f2fd
    style D fill:#fff3e0
    style E fill:#fff3e0
    style F fill:#fff3e0
    style G fill:#f1f8e9
    style H fill:#f1f8e9
    style I fill:#f1f8e9
    style J fill:#f1f8e9
    style K fill:#f3e5f5
    style L fill:#f3e5f5
    style M fill:#f3e5f5
```

## 📈 Performance Monitoring

```mermaid
graph LR
    subgraph "Input Metrics"
        A[API Calls]
        B[Processing Time]
        C[Success Rates]
        D[Error Counts]
    end
    
    subgraph "Processing"
        E[Data Collection]
        F[Analysis]
        G[Reporting]
    end
    
    subgraph "Output"
        H[Performance Dashboard]
        I[Alert System]
        J[Optimization Suggestions]
    end
    
    A --> E
    B --> E
    C --> E
    D --> E
    
    E --> F
    F --> G
    
    G --> H
    G --> I
    G --> J
    
    style A fill:#e3f2fd
    style B fill:#e3f2fd
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style E fill:#f3e5f5
    style F fill:#f3e5f5
    style G fill:#f3e5f5
    style H fill:#e8f5e8
    style I fill:#e8f5e8
    style J fill:#e8f5e8
```

## 🛡️ Security & Compliance

```mermaid
graph TB
    subgraph "Security Layers"
        A[Environment Variables]
        B[OAuth2 Authentication]
        C[API Key Management]
        D[Rate Limiting]
    end
    
    subgraph "Compliance Checks"
        E[Content Filtering]
        F[Brand Safety]
        G[Legal Compliance]
        H[Community Guidelines]
    end
    
    subgraph "Monitoring"
        I[Audit Trail]
        J[Error Logging]
        K[Performance Tracking]
    end
    
    A --> B
    B --> C
    C --> D
    
    D --> E
    E --> F
    F --> G
    G --> H
    
    E --> I
    F --> I
    G --> I
    H --> I
    
    I --> J
    J --> K
    
    style A fill:#e3f2fd
    style B fill:#e3f2fd
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style E fill:#fff3e0
    style F fill:#fff3e0
    style G fill:#fff3e0
    style H fill:#fff3e0
    style I fill:#e8f5e8
    style J fill:#e8f5e8
    style K fill:#e8f5e8
```

---

*These diagrams provide a comprehensive visual understanding of the Twitter Automation Pipeline's architecture, workflow, and components.* 