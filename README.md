# japanese-tutor-rag-agent

## Overview

An interactive Japanese language tutor project that documents the development of the project. Starting from simple prompt engineering to a fully developed context aware Agent. 

It will also serve as a way to demonstrate MLOPS practices that simulate a real development workflows to maintain security, speed up development and intergrate new features in a seamless way for users.

## Usage

Steps to run the project:

1. first copy the `.env.example` into a new file called `.env` and fill in the necessary values inside like your own API keys.

2. Ensure you have the `uv` package manager installed and run:
   ```bash
   uv sync
   ```

3. Finally you can run the project by:
   ```bash
   uv run python -m src.main
   ```

## Projects AI Usage

AI has not been used to write any code in this project. This project serves as a learning experience for developing LLM experiences and agents. Using AI would take away from that learning experience.

However, AI assistance has been used in other ways to give advice on ideas, suggest best software practices and finding documentation.