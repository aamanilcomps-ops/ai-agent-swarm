# 🤖 SwarmMind: Autonomous Multi-Agent AI System

An advanced, futuristic AI workflow engine built entirely inside a mobile terminal environment using Termux. SwarmMind orchestrates a network of specialized AI agents that collaborate, critique, and execute complex problem-solving pipelines autonomously.

## 🚀 Features
- **Multi-Agent Orchestration**: Independent agents with unique system prompts, goals, and constraints.
- **Hierarchical Planning**: A Manager agent breaks down user prompts into a logical sequence of tasks.
- **Termux-Optimized**: Lightweight, high-throughput execution designed for mobile command centers via cloud API bindings.

## 📁 Repository Structure
- `config/`: Contains YAML definitions for agent personas.
- `src/`: Houses core runtime logic for agent execution and task handling.

## 🛠️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com
   cd ai-agent-swarm
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   nano .env # Add your API Key here
   ```

4. **Run the Project**
   ```bash
   python src/main.py
   ```
