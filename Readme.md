# AI Robotic Task Planner

An AI-powered robotic task planning system that converts natural language commands into structured robot actions and executes them in a PyBullet simulation.

## Project Overview

This project allows a user to give a natural language command such as:

```text
move the bottle to the tray
```

The system converts the command into a structured JSON task plan, validates the plan, and then executes it using a Franka Panda robotic arm in PyBullet simulation.

The main goal is to make robotic task execution more flexible, safe, and user-friendly by using an AI planner with validation before execution.

## Current Features

- Natural language command input
- Qwen 2.5 based LLM planner through Ollama
<<<<<<< HEAD
- Rule-based fallback plannerV
=======
- Rule-based fallback planner
>>>>>>> 875ecccd2bf45227be5246ed5e6532b50a076443
- JSON task plan generation
- Task plan validation before execution
- PyBullet simulation with Franka Panda robotic arm
- Multiple objects and target locations
- Object pick-and-place workflow
- Execution logging
- Flask-based frontend dashboard
- Modern dark theme UI
- Execute simulation directly from frontend

## System Architecture

```text
User Command
     ↓
Qwen 2.5 / Rule-Based Planner
     ↓
JSON Task Plan
     ↓
Plan Validator
     ↓
Action Executor
     ↓
Robot Controller
     ↓
PyBullet Simulation
     ↓
Frontend Dashboard
```

## Example

User command:

```text
move the bottle to the tray
```

Generated JSON task plan:

```json
{
    "steps": [
        {
            "action": "pick",
            "object": "bottle"
        },
        {
            "action": "place",
            "location": "tray"
        }
    ]
}
```

## Project Structure

```text
Project/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── templates/
│   └── index.html
│
├── simulation/
│   ├── test.py
│   ├── world.py
│   ├── robot_controller.py
│   ├── action_executor.py
│   ├── command_runner.py
│   ├── llm_planner.py
│   ├── model_config.py
│   ├── plan_validator.py
│   └── execution_logger.py
```

## File Description

### `app.py`

Main Flask application. It connects the frontend with the planning pipeline, validation system, execution logging, and PyBullet simulation launcher.

### `templates/index.html`

Frontend dashboard where users can enter commands, generate JSON task plans, view validation results, and start the simulation.

### `simulation/test.py`

Main simulation runner. It loads PyBullet, the Franka Panda robot, objects, target locations, and executes the generated task plan.

### `simulation/world.py`

Defines available objects and target locations in the simulation environment.

### `simulation/robot_controller.py`

Contains low-level robot control functions such as moving the robot arm, opening and closing the gripper, attaching objects, and releasing objects.

### `simulation/action_executor.py`

Converts high-level JSON actions into robot movement functions.

### `simulation/command_runner.py`

Rule-based fallback planner. It converts simple known commands into JSON task plans without using an LLM.

### `simulation/llm_planner.py`

LLM planner that uses Qwen 2.5 through Ollama to convert natural language commands into JSON task plans.

### `simulation/model_config.py`

Stores model configuration such as model name and Ollama API URL.

### `simulation/plan_validator.py`

Validates the generated JSON task plan before execution. It checks valid actions, available objects, and available locations.

### `simulation/execution_logger.py`

Logs user commands, planner used, generated task plan, and validation result.

## Supported Objects

```text
bottle
cup
box
```

## Supported Locations

```text
tray
left
right
center
```

## Demo Commands

```text
move the bottle to the tray
place the cup on the left
put the box on the right
move the phone to the tray
```

The last command is used to test validation failure because `phone` is not a supported object.

## Tech Stack

- Python
- Flask
- PyBullet
- Qwen 2.5
- Ollama
- HTML
- CSS
- JSON
- GitHub

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/harsh2370/ai-robotic-task-planner.git
cd ai-robotic-task-planner
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

For Windows PowerShell:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start Ollama model

Check installed models:

```bash
ollama list
```

If Qwen is not available:

```bash
ollama pull qwen2.5:7b
```

## How to Run

### Run frontend dashboard

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

### Run simulation manually

```bash
python simulation/test.py "move the bottle to the tray"
```

## Current Status

The project currently supports an end-to-end workflow from natural language command input to validated JSON task generation and PyBullet robot execution through a web dashboard.

## Future Improvements

- Improve natural language command handling
- Add more objects and target locations
- Add more robotic actions
- Improve simulation speed
- Add cloud-based LLM support
- Integrate ROS 2 or MoveIt for real robot compatibility
<<<<<<< HEAD
- Use execution logs to build a project-specific dataset
=======
- Use execution logs to build a project-specific dataset
>>>>>>> 875ecccd2bf45227be5246ed5e6532b50a076443
