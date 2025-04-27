# User Guide: Python Project Starter

This guide is designed for non-technical users who want to create and maintain Python projects following best practices, without having to learn all the complexities of modern Python development workflows.

## Table of Contents

- [Understanding Key Concepts](#understanding-key-concepts)
- [Installation](#installation)
- [Creating Your First Project](#creating-your-first-project)
- [Adding Code to Your Project](#adding-code-to-your-project)
- [Saving Your Changes](#saving-your-changes)
- [Sharing Your Project](#sharing-your-project)
- [Collaborating with Others](#collaborating-with-others)
- [Checking Project Status](#checking-project-status)
- [Troubleshooting](#troubleshooting)

## Understanding Key Concepts

Before we begin, let's clarify a few concepts that will help you understand what Python Project Starter (PPS) does:

### Python Project Structure

A well-organized Python project has a specific structure that makes it easier to maintain and share. PPS automatically creates this structure for you, including:

- A **src folder** that contains your actual Python code
- A **tests folder** for testing your code
- A **pyproject.toml file** that defines your project's configuration
- A **README.md file** that explains what your project does

### Version Control with Git

Git is a tool that tracks changes to your code over time. It's essential for:

- Keeping a history of your changes
- Collaborating with others
- Backing up your code

PPS simplifies Git commands into easy-to-understand operations like "save" and "sync".

### Virtual Environments

A virtual environment is an isolated space where Python packages can be installed without affecting your entire system. PPS sets this up automatically using a tool called "UV".

## Installation

### Step 1: Install Python

If you don't have Python installed:

1. Download Python 3.10 or higher from [python.org](https://www.python.org/downloads/)
2. During installation, make sure to check "Add Python to PATH"

### Step 2: Install Git

If you don't have Git installed:

1. Download Git from [git-scm.com](https://git-scm.com/downloads)
2. Use the default installation options

### Step 3: Install UV (Optional but Recommended)

UV is a faster, more modern tool for managing Python packages:

```bash
# In your command prompt or terminal, run:
pip install uv
```

### Step 4: Install Python Project Starter

```bash
# Using pip
pip install python-project-starter

# Or if you installed UV
uv pip install python-project-starter
```

## Creating Your First Project

### Basic Project Creation

1. Open your command prompt or terminal
2. Navigate to where you want to create your project
3. Run the command:

```bash
pps new my_project
```

Replace `my_project` with your desired project name (use lowercase letters and underscores).

### What Happens When You Create a Project

When you run `pps new`, several things happen automatically:

1. A new folder is created with your project name
2. The proper Python project structure is set up inside that folder
3. Git is initialized to track your changes
4. A virtual environment is created to manage dependencies
5. Basic development tools are installed

### Creating a Project in a Specific Location

If you want to create your project in a specific folder:

```bash
pps new my_project --dir C:\Users\YourName\Projects
```

## Adding Code to Your Project

After creating your project:

1. Navigate into your project folder:
   ```bash
   cd my_project
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On Mac/Linux:
     ```bash
     source .venv/bin/activate
     ```

3. Create or edit your Python files in the `src/my_project/` folder

## Saving Your Changes

After making changes to your code:

1. Ensure you're in your project directory
2. Run:
   ```bash
   pps save -m "Added new feature"
   ```

Replace "Added new feature" with a brief description of what you changed.

### What Happens When You Save

When you run `pps save`, PPS:

1. Identifies all the files you've changed
2. Records those changes in Git
3. Creates a "commit" with your message that describes what changed

## Sharing Your Project

### Setting Up a Remote Repository

Before you can share your project, you need to create a repository on a service like GitHub:

1. Go to [GitHub](https://github.com/) and sign up if you haven't already
2. Click the "+" icon in the top right and select "New repository"
3. Name your repository (typically the same as your project)
4. Don't initialize with README or other files (your project already has these)
5. Click "Create repository"
6. Follow the instructions under "…or push an existing repository from the command line"

### Syncing Your Changes

Once your remote repository is set up, you can sync your changes:

```bash
pps sync
```

This command both pulls changes from others (if any) and pushes your local changes to the remote repository.

## Collaborating with Others

### Downloading Someone Else's Project

To work with an existing project:

1. Get the repository URL from GitHub
2. In your command prompt or terminal, run:
   ```bash
   git clone https://github.com/username/project-name.git
   cd project-name
   ```

3. Set up the project environment:
   ```bash
   uv venv
   uv sync --dev
   ```

4. Now you can use PPS commands like `save` and `sync`

### Workflow for Collaboration

1. Always run `pps sync` before starting work to get the latest changes
2. Make your changes to the code
3. Use `pps save -m "Description of changes"` to record your changes
4. Use `pps sync` to share your changes and get any new changes from collaborators

## Checking Project Status

To see what files you've changed and haven't saved yet:

```bash
pps status
```

This will show you:
- Which files have been modified
- Whether the project structure is correct
- If there are any issues with your Git setup

## Troubleshooting

### Common Issues

#### "Command not found" when running pps

The `pps` command may not be in your system's PATH. Try:
```bash
python -m project_starter <command>
```

#### Changes not showing up for collaborators

Make sure you've run both:
```bash
pps save -m "Your message"
pps sync
```

#### Virtual environment issues

If your virtual environment isn't working properly:
```bash
# Recreate the virtual environment
uv venv
uv sync --dev
```

#### Git authentication errors

If you're having trouble pushing to GitHub:
1. Make sure you're logged in to GitHub
2. Check that you have the correct permissions for the repository
3. Ensure you've set up SSH keys or stored your credentials

### Getting Help

If you encounter an issue not covered here:
1. Run the command with `--help` for more information:
   ```bash
   pps --help
   pps new --help
   ```
2. Check the project's GitHub issues page
3. Reach out to your technical team member if you have one

## Next Steps

As you become more comfortable with PPS, you might want to:

1. Learn more about Python programming
2. Explore more advanced Git features
3. Add testing to your project
4. Set up continuous integration

Remember that PPS is designed to help you focus on writing code rather than managing project infrastructure, so you can gradually learn these more advanced concepts as needed. 