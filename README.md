# DIAL Agent Implementation

## 🎯 Task Overview

With this task you will create AI agent with custom tool, MCP tools and DIAL deployment tools, practice with streaming
in Choice and Stage in DIAL Chat.

## 🎓 Learning Goals

By completing this project, you will learn:

- **AI Agent Architecture**: Building intelligent agents that can orchestrate multiple tools
- **Tool Orchestration**: Combining MCP tools, custom tools and deployment-based tools (web search, image generation)
- **Streaming & Real-time Processing**: Handling streaming responses and real-time tool execution
- **DIAL Integration**: Working with DIAL API for AI model interactions


## 📋 Requirements

- **Python**: 3.11 or higher
- **Docker & Docker Compose**: For containerized deployment
- **API Access**:
    - DIAL API key with appropriate permissions
    - EPAM VPN connection for internal API access
- **Optional**: Postman for API testing

## 🚀 Getting Started

### 1. Environment Setup

```bash
pip install -r requirements.txt
```

### 2. API Configuration

1. **Connect to EPAM VPN** (required for internal API access)
2. **Obtain DIAL API Key** from EPAM support and set it as env `DIAL_API_KEY` variable
3. **Set environment variables**:

# ✍️ Implementation Tasks
**PAY ATTENTION THAT FULL IMPLEMENTATION OF THIS AGENT WILL TAKE 4+ HOURS**

<details>
<summary>Step 1: Simple Agent with one custom tool</summary>

### Task 1: Implement Base Tool

Implement all `TODO` in [task/tools/base.py](task/tools/base.py):

### Task 2: Implement Calculator Tool

Implement all `TODO` in [task/tools/calculator.py](task/tools/calculator.py):

Sample of the properties configuration:

```json
{
  "type": "object",
  "properties": {
    "param1": {
      "type": "number",
      "description": "Your param description"
    },
    "param2": {
      "type": "string",
      "description": "Your param description",
      "enum": [
        "val1",
        "val2",
        "val3"
      ]
    }
  },
  "required": [
    "param1",
    "param2"
  ]
}
```

### Task 3: Implement LLM Agent

Implement all `TODO` in [task/llm_agent.py](task/llm_agent.py)

### Task 4: Complete Application Setup

Implement all `TODO` for **STEP 1** in [task/app.py](task/app.py)

### Task 5: Configure DIAL Core

Add in the [core/config.json](core/config.json) such configurations:

- In the `applications` block:
    ```
    "super-agent": {
          "displayName": "Super Agent",
          "description": "Super Agent. Works with different DIAL Deployments, works with MCP tools, and performs simple calculations.",
          "endpoint": "http://host.docker.internal:5030/openai/deployments/super-agent/chat/completions",
          "inputAttachmentTypes": [
            "image/png",
            "image/jpeg"
          ]
        }
    ```
- In the `models` block:
    ```
     "gpt-4o": {
          "displayName": "GPT 4o",
          "endpoint": "http://adapter-dial:5000/openai/deployments/gpt-4o/chat/completions",
          "iconUrl": "http://localhost:3001/gpt4.svg",
          "type": "chat",
          "upstreams": [
            {
              "endpoint": "https://ai-proxy.lab.epam.com/openai/deployments/gpt-4o/chat/completions",
              "key": "YOUR_API_KEY"
            }
          ]
        }
    ```
- Don't forget to replace `YOUR_API_KEY` with your DIAL API Key

### Task 6: Run compose with local DIAL 

Run [docker-compose.yml](docker-compose.yml) such configurations:
```bash
docker compose up -d
```

### Task 7: Check that DIAL is working locally
- Run [task/app.py](task/app.py) locally
- Open http://localhost:3000/
- Test that GPT model is available and provides responses
- Test Super Agent application:
    ```text
    Hi, what can you do?
    ```
- Try to call calculator tool:
    ```text
    Calculate 495903.928834 * 39483.1038472
    ```
- Try to analyze picture (you need to upload picture for analyze, in Core configuration we allowed uploading `png` and `jpeg` files):
    ```text
    What do you see here?
    ```

</details>

<details>
<summary>Step 2: Add deployment tools</summary>

### Task 1: Implement Deployment Tool

Implement all `TODO` in [task/tools/deployment/base.py](task/tools/deployment/base.py)

### Task 2: Implement Web Search Deployment Tool

Implement all `TODO` in [task/tools/deployment/web_search.py](task/tools/deployment/web_search.py)

### Task 3: Implement Image Generation Deployment Tool

Implement all `TODO` in [task/tools/deployment/image_generation.py](task/tools/deployment/image_generation.py)

### Task 4: Complete Application Setup

Implement all `TODO` for **STEP 2** in [task/app.py](task/app.py)

### Task 5: Configure DIAL Core

Add in the [core/config.json](core/config.json) such configurations:

- In the `models` block:
    ```
    "gemini-2.0-flash-exp-google-search": {
      "displayName": "Gemini 2.0 Web Search",
      "endpoint": "http://adapter-dial:5000/openai/deployments/gemini-2.0-flash-exp-google-search/chat/completions",
      "iconUrl": "http://localhost:3001/Gemini-Pro-Vision.svg",
      "type": "chat",
      "upstreams": [
        {
          "endpoint": "https://ai-proxy.lab.epam.com/openai/deployments/gemini-2.0-flash-exp-google-search/chat/completions",
          "key": "YOUR_API_KEY"
        }
      ]
    },
    "dall-e-3": {
      "displayName": "DALL-E",
      "endpoint": "http://adapter-dial:5000/openai/deployments/dall-e-3/chat/completions",
      "iconUrl": "http://localhost:3001/gpt3.svg",
      "type": "chat",
      "upstreams": [
        {
          "endpoint": "https://ai-proxy.lab.epam.com/openai/deployments/dall-e-3/chat/completions",
          "key": "YOUR_API_KEY"
        }
      ]
    }
    ```
- Don't forget to replace `YOUR_API_KEY` with your DIAL API Key

### Task 6: Restart compose with updated local DIAL

```bash
docker compose stop && docker compose up -d --build
```

### Task 7: Check Agent with DIAL deployments tools
- Run [task/app.py](task/app.py) locally
- Open http://localhost:3000/
- Test them:
    ```text
    What is the weather in Kyiv now?
    ```
    ```text
    Generate an image in high quality with smiling elephant
    ```

</details> 

<details>
<summary>Step 3: Add MCP tools</summary>

### Task 1: Complete MCP Server Setup

Implement and run the MCP server with three tools:

- `reverse_string`: Reverses text input
- `random_num`: Generates random numbers
- `is_palindrome`: Checks if text is a palindrome

1. Implement all `TODO` in [mcp_server/server.py](mcp_server/server.py)
2. Start the MCP server:
   ```bash
   cd ./mcp_server/
   ```
   ```bash
   docker compose up -d
   ```
3. Verify server is running:
   ```bash
   docker compose ps -a
   ```

### Task 2: Implement MCP Client

Implement all `TODO` in [task/tools/mcp/mcp_client.py](task/tools/mcp/mcp_client.py)

### Task 3: Implement MCP Tool

Implement all `TODO` in [task/tools/mcp/mcp_tool.py](task/tools/mcp/mcp_tool.py)

### Task 4: Complete Application Setup

Implement all `TODO` for **STEP 3** in [task/app.py](task/app.py)

### Task 5: Check Agent with MCP tools
- Run [task/app.py](task/app.py) locally
- Open http://localhost:3000/
- Test them:
    ```text
    Generate a random number between 1 and 100
    ```
    ```text
    Check if "racecar" is a palindrome
    ```
    ```text
    Generate a random number, then by this number search 'Magic of the {number}' and then based on the description generate an image
    ```
</details>

---

# 🧪 Testing Scenarios

### Basic Calculator Operations

```
Calculate 495903.928834 * 39483.1038472
```

### Web Search Integration

```
What is the weather in Kyiv now?
```

### MCP Tool Testing

```
Generate a random number between 1 and 100, then check if "racecar" is a palindrome
```

### Complex Multi-Tool Requests

```
Generate a random number, then by this number search 'Magic of the {number}' and then based on the description generate an image
```

### Add in Chat some picture (png or jpeg)

```
What do you see here?
```

---

# <img src="dialx-banner.png">