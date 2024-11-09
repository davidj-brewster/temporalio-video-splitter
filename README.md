# Temporal Video Processing 

A demonstration of using Temporal.io for orchestrating video processing workflows. This project shows how to structure long-running video processing tasks using Temporal's workflow engine.
Actually had started on this due to being stuck on a more complicated project and needed to figure how to get the basic interactions working between temporal IO components (Workflows, Workers and Activities).

## Architecture

The system consists of three main components:
1. Workflow Starter (start_workflow.py)
2. Worker Process (worker.py)
3. Activity Definitions (activities.py)

## System Architecture Diagram

The diagram above shows how the different components interact through the Temporal server.

## Workflow Process

The following diagram shows the video processing workflow sequence, including retry logic and state transitions.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt #or use uv ;) 
```

2. Ensure Temporal server is running at localhost:7233

## Usage

1. Start the worker process:
```bash
python worker.py
```

2. In a separate terminal, start the workflow:
```bash
python start_workflow.py
```

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

```
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

```
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
