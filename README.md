# ToDoList

---

## Purpose

ToDoList is a lightweight GUI task manager designed for quickly creating and organizing nested lists of tasks.

Tasks are organized into projects and subprojects using a hierarchical folder structure. Each task can contain additional attributes such as:

- Description
- Deadline
- Duration
- Priority
- Attachments
- Label
- Color

The goal is to provide a simple, quickly accessible task manager without the overhead of a larger task-management application.

---

## Features

### Projects and Subprojects

Projects are represented as folders inside the `Tasks` directory. Folders can be nested to create subprojects.

Example:

    Tasks/
    ├── School/
    │   ├── Math/
    │   ├── Physics/
    │   └── Computer Science/
    ├── Work/
    │   ├── Project A/
    │   └── Project B/
    └── Personal/

Selecting a project displays the tasks contained in that folder and its subprojects.

### Tasks

Each task has a required name and several optional attributes:

| Attribute | Description |
|---|---|
| Name | The name of the task |
| Description | Additional information about the task |
| Deadline | The date the task is due |
| Duration | Estimated task duration in minutes |
| Priority | A priority value from 1–10 |
| Attachments | File paths associated with the task |
| Label | A short category or description |
| Color | A color associated with the task |

### Task Sorting

Tasks are currently sorted by deadline.

Tasks without a deadline are placed after tasks with deadlines.

---

## Setup

### macOS

The project includes setup and run scripts for macOS.

From the project root, run:

    ./scripts/mac_setup.sh

The setup script creates the Python virtual environment and installs the dependencies listed in `requirements.txt`.

After setup, the application can be launched using:

    ./scripts/mac_run.sh

### Manual Setup

If the setup script is not used, create a virtual environment manually:

    python3 -m venv venvTask

Activate it:

    source venvTask/bin/activate

Then install the required packages:

    pip install -r requirements.txt

---

## Project Structure

    ├── README.md
    ├── config.py
    ├── requirements.txt
    ├── scripts
    │   ├── mac_run.sh
    │   └── mac_setup.sh
    └── src
        ├── __init__.py
        ├── app_state.py
        ├── attributeView
        │   └── attributeView.py
        ├── main.py
        ├── projectTree
        │   └── projectTree.py
        ├── system
        │   └── filesystem.py
        ├── taskView
        │   ├── Task.py
        │   ├── task_widgets.py
        │   └── tasks_view.py
        └── window.py

---

## Architecture

The application is divided into several primary components.

### `window.py`

Contains `MainWindow`, which assembles the major parts of the application:

    ┌─────────────────┬──────────────────────┬─────────────────────┐
    │                 │                      │                     │
    │  Project Tree   │      Tasks View      │   Attribute View    │
    │                 │                      │                     │
    │  Projects       │      Task List       │   Task Information  │
    │  Subprojects    │      Add Task        │   Edit Task         │
    │                 │                      │                     │
    └─────────────────┴──────────────────────┴─────────────────────┘

`MainWindow` also connects signals between the different views.

### `projectTree.py`

Contains `ProjectTree`, which provides the hierarchical project and subproject interface.

It is responsible for:

- Displaying the `Tasks` directory as a tree
- Selecting projects
- Creating folders
- Removing folders
- Maintaining expanded folder state

Selecting a folder emits its path to `TasksView`, which then loads the associated tasks.

### `tasks_view.py`

Contains `TasksView`, which manages the central task list.

It is responsible for:

- Loading tasks from project folders
- Displaying task widgets
- Creating new tasks
- Removing tasks
- Selecting tasks
- Sorting tasks
- Saving task data

When a project is selected, `TasksView` recursively searches the selected folder for task data and displays all tasks belonging to that project and its subprojects.

### `Task.py`

Contains the `Task` data model and `TaskSerializer`.

`Task` represents an individual task with attributes such as:

    Task(
        name,
        deadline,
        duration,
        description,
        color,
        basePriority,
        attachments,
        label
    )

`TaskSerializer` converts between `Task` objects and dictionaries for persistent storage.

### `task_widgets.py`

Contains `TaskItem`, the Qt widget used to visually represent an individual task.

A task widget provides:

- A completion checkbox
- The task name
- Task selection behavior

### `attributeView.py`

Contains `AttributeView`, which displays and edits the attributes of the currently selected task.

The view currently supports editing:

- Name
- Description
- Deadline
- Priority
- Duration
- Attachments

Changes are emitted through the `taskUpdated` signal.

### `app_state.py`

Contains `AppState`, which stores application-wide state shared between the different views.

Currently it stores:

    selected_folder
    selected_task
    sort_mode
    tasks

This prevents each view from maintaining its own separate copy of the application's task state.

### `filesystem.py`

Contains the functions responsible for reading and writing task data to the filesystem.

The GUI does not directly handle the task file format. Instead, `TasksView` uses the filesystem functions to load and save task data.

---

## Data Storage

Projects and tasks are stored under the `Tasks` directory specified by the application's configuration.

The root directory is constructed using:

    Path(config.rootPath) / "Tasks"

Each project or subproject corresponds to a directory.

Task information is stored within these directories by the filesystem module.

---

## Application State

`AppState` is shared between the main views.

The current state consists of:

    class AppState:
        selected_folder
        selected_task
        sort_mode
        tasks

The general data flow is:

    ProjectTree
         │
         │ selected project
         ▼
    AppState.selected_folder
         │
         ▼
    TasksView
         │
         │ load tasks
         ▼
    AppState.tasks
         │
         ▼
    TaskItem widgets
         │
         │ select task
         ▼
    AppState.selected_task
         │
         ▼
    AttributeView

When an attribute is changed, the updated `Task` object is sent back through the application and saved.

---

## Dependencies

The project uses Python and PySide6 for the graphical interface.

Additional dependencies are listed in:

    requirements.txt

Install them with:

    pip install -r requirements.txt

---

## Configuration

Application configuration is contained in:

    config.py

The configuration determines values such as the root location used by the application.

The `Tasks` directory is created relative to the configured root path:

    task_root = Path(config.rootPath) / "Tasks"

---

## Running the Application

On macOS, after completing setup:

    ./scripts/mac_run.sh

Alternatively, with the virtual environment activated, the application can be run through the project's Python entry point.

---

## Current Limitations

The project is still under development. Some functionality and UI behavior may change as the application evolves.

Current functionality primarily focuses on:

- Nested project organization
- Task creation and removal
- Task selection
- Task attributes
- Deadline sorting
- Persistent task storage
- File attachments

---

## Future Improvements

Potential future features include:

- More sorting options
- Filtering tasks
- Task completion persistence
- Custom task colors
- Labels and categories
- Improved attachment management
- Recurring tasks
- More detailed deadline/time support
- Drag-and-drop project organization
- Search functionality
- Additional task views
- Improved cross-platform setup scripts

---

## Technology

- **Python**
- **PySide6**
- **JSON/filesystem-based persistence**
- **Object-oriented application architecture**