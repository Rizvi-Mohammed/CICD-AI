# CICD-AI

![alt text](https://github.com/Rizvi-Mohammed/CICD-AI/blob/main/codetoflow.png?raw=true)

# AI-Enhanced CI/CD Pipeline

A lightweight CI/CD pipeline with integrated AI assistance for code analysis, security scanning, and deployment risk assessment.

## Features

- 🧠 AI-powered code quality suggestions
- 🔐 Intelligent security vulnerability analysis
- 🧪 Smart test coverage recommendations
- 🏗️ Infrastructure as Code validation
- 🚀 Risk-based deployment decisions

## Requirements

- Python 3.8+
- AWS Account with Bedrock access
- Git
- Docker (optional)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-cicd-pipeline.git
cd ai-cicd-pipeline

# Install dependencies
pip install -e .

# Set up AWS credentials
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-west-2
```

### Configuration

Edit `configs/default.yaml` to adjust default settings or create a custom config:

```yaml
# Example config override
ai:
  model: claude-3-sonnet-20240229
  risk_threshold: 3
repositories:
  default_branch: main
```

### Basic Usage

#### Command Line

Run the pipeline on a repository:

```bash
ai-cicd run --repo https://github.com/your-org/your-repo.git --branch main
```

#### Web Interface

Start the web server:

```bash
ai-cicd server --port 8080
```

Then navigate to `http://localhost:8080` in your browser.

## Integrating with Existing CI/CD Systems

### GitHub Actions

Add this to your `.github/workflows/ai-pipeline.yml`:

```yaml
name: AI CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  ai-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install git+https://github.com/yourusername/ai-cicd-pipeline.git
      - name: Run AI analysis
        run: |
          ai-cicd run --repo $GITHUB_REPOSITORY --branch $GITHUB_REF_NAME --output-format json > ai-results.json
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: us-west-2
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: ai-analysis-results
          path: ai-results.json
```

### Jenkins

Add this to your Jenkinsfile:

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
        }
    }
    stages {
        stage('Setup') {
            steps {
                sh 'pip install git+https://github.com/yourusername/ai-cicd-pipeline.git'
            }
        }
        stage('AI Analysis') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh 'ai-cicd run --repo ${GIT_URL} --branch ${GIT_BRANCH} --output-file ai-results.json'
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'ai-results.json'
        }
    }
}
```

## Architecture

The pipeline consists of these main components:

1. **Pipeline Orchestrator**: Coordinates all stages and manages the overall flow
2. **Code Analyzer**: Performs static analysis and linting
3. **Security Scanner**: Detects vulnerabilities in code and dependencies
4. **Test Manager**: Runs tests and analyzes coverage
5. **Deployment Manager**: Validates and deploys infrastructure
6. **AI Assistant**: Enhances each stage with intelligent insights

## Extending the Pipeline

### Adding a New Analyzer

1. Create a new module in `src/modules/your_analyzer.py`
2. Implement the analyzer interface
3. Register your analyzer in `src/main.py`

Example:

```python
# src/modules/performance_analyzer.py
from .base_analyzer import BaseAnalyzer

class PerformanceAnalyzer(BaseAnalyzer):
    def analyze(self, repo_path):
        # Implement performance analysis
        return {
            "issues": [...],
            "metrics": {...}
        }

# In src/main.py
from modules.performance_analyzer import PerformanceAnalyzer
# ...
self.performance_analyzer = PerformanceAnalyzer()
# Add to pipeline stages
```

## License

MIT
