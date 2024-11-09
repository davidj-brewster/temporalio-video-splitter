# Temporal Video Processing 

A demonstration of using Temporal.io for orchestrating video processing workflows. This project shows how to structure long-running video processing tasks using Temporal's workflow engine.

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

### State diagram

```mermaid

stateDiagram-v2
    [*] --> StartWorkflow: Launch
    
    StartWorkflow --> AnalyzeVideo: Execute Activity 1
    note right of AnalyzeVideo
        Extract video metadata:
        - dimensions
        - fps
        - duration
    end note
    
    AnalyzeVideo --> ExtractFrames: Execute Activity 2
    note right of ExtractFrames
        - Read video frames
        - Save to disk
        - Report progress
    end note
    
    ExtractFrames --> ProcessFrames: Execute Activity 3
    note right of ProcessFrames
        - Apply processing
        - Save results
        - Track progress
    end note
    
    ProcessFrames --> Complete: Return Results
    Complete --> [*]
    
    state RetryLoop <<fork>>
        AnalyzeVideo --> RetryLoop: Failure
        ExtractFrames --> RetryLoop: Failure
        ProcessFrames --> RetryLoop: Failure
        RetryLoop --> [*]: Max Retries
        RetryLoop --> AnalyzeVideo: Retry
        RetryLoop --> ExtractFrames: Retry
        RetryLoop --> ProcessFrames: Retry
    end state
```

### Architecture

```mermaid
flowchart TB
    subgraph Client
        SW[Start Workflow\nstart_workflow.py]
    end
    
    subgraph "Temporal Server"
        TS[Temporal Service]
        TQ[Task Queue:\nvideo-processing-queue]
    end
    
    subgraph "Worker Node"
        W[Worker Process\nworker.py]
        ACT[Activities\nactivities.py]
        WF[Workflow Definition\nworkflows.py]
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
