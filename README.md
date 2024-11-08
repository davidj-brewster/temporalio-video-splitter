# temporalio-video-splitter
Split video into frames using temporalio for orchestration - exemplary project

## Installation

```
brew install temporalio
pip install -r requirements.txt
```

## Usage

Start temporal dev-server
```
temporal server start-dev
```
Start workflow
```
python ./start_workflow.py
```
Place a video file "input.mp4" in the directory of the script.

Start worker
```
python ./worker.py
```
