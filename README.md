# Temporal Video Processing 

A demonstration of using Temporal.io for orchestrating video processing workflows. This project shows how to structure long-running video processing tasks using Temporal's workflow engine.
Actually had started on this due to being stuck on a more complicated project and needed to figure how to get the basic interactions working between temporal IO components (Workflows, Workers and Activities) - essentially copied another project with the help of a "cloudy" copilot and figured this looks pretty nice after all.. :D 

## Architecture

Three main components like in every good Temporal.io implementation ;):
1. Workflow init job (start_workflow.py)
2. Worker Process (worker.py)
3. Activity Defn's (activities.py)

## Installation / usage

1. Install dependencies:
```bash
pip install -r requirements.txt #or use uv ;) 
```

2. Ensure Temporal server is running at localhost:7233

3. Start the worker process:
```bash
python worker.py
```

4. In a separate terminal, start the workflow:
```bash
python start_workflow.py
```

The video location is hardcoded but who cares because nobody will see this. It's easy to change ;) 

## Components

### start_workflow.py
- Entry point for starting workflow executions
- Connects to Temporal server, starts workflow and waits for results

### worker.py
- Long-running process that executes waits for work and fires/monitors activities under a task-queue

### workflows.py
- Defines workflow structure and sequencing
- Orchestrates actual activity execution

### activities.py
- Implements individual processing tasks
- Reports progress via heartbeats

## Features

- Well seperated architecture, simple enough to copy as a template
- Automatic retries
- Progress tracking and heartbeats

## Error Handling

The system includes comprehensive error handling:
- Automatic retries, exponential backoff
- Activity timeouts
- Progress monitoring

## Monitoring

Monitor workflow execution through:
- Temporal Web UI
- Worker logs and temporal server log

## Some diagrams (thanks Claude)

### State Flow

```mermaid
stateDiagram-v2
    [*] --> StartWorkflow
    StartWorkflow --> AnalyzeVideo
    
    note right of AnalyzeVideo
        Extract metadata:
        dimensions, fps, duration
    end note
    
    AnalyzeVideo --> ExtractFrames
    note right of ExtractFrames
        Read and save frames
        Report progress
    end note
    
    ExtractFrames --> ProcessFrames
    note right of ProcessFrames
        Process frames
        Save results
    end note
    
    ProcessFrames --> Complete
    Complete --> [*]
    
    AnalyzeVideo --> Retry: Failure
    ExtractFrames --> Retry: Failure
    ProcessFrames --> Retry: Failure
    Retry --> [*]: Max Retries
    Retry --> AnalyzeVideo
    Retry --> ExtractFrames
    Retry --> ProcessFrames
```

### Architecture

```mermaid
graph TD
    subgraph Client
        SW[Start Workflow<br/>start_workflow.py]
    end
    
    subgraph "Temporal Server"
        TS[Temporal Service]
        TQ[Task Queue:<br/>video-processing-queue]
    end
    
    subgraph "Worker Node"
        W[Worker Process<br/>worker.py]
        ACT[Activities<br/>activities.py]
        WF[Workflow Definition<br/>workflows.py]
    end
    
    SW -->|1. Start Workflow| TS
    TS -->|2. Queue Tasks| TQ
    W -->|3. Poll for Tasks| TQ
    TQ -->|4. Deliver Tasks| W
    W -->|5. Execute| WF
    WF -->|6. Call| ACT
    ACT -->|7. Results| W
    W -->|8. Report Status| TS
    TS -->|9. Return Results| SW
```	
