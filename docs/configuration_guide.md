# Configuration Guide

## Quick Settings

Copy the `conf.yaml.example` file to `conf.yaml` and modify the configurations to match your specific settings and requirements.

```bash
cd deer-flow
cp conf.yaml.example conf.yaml
```

## Which models does DeerFlow support?

In DeerFlow, currently we only support non-reasoning models, which means models like OpenAI's o1/o3 or DeepSeek's R1 are not supported yet, but we will add support for them in the future.

### Supported Models

`doubao-1.5-pro-32k-250115`, `gpt-4o`, `qwen-max-latest`, `gemini-2.0-flash`, `deepseek-v3`, and theoretically any other non-reasoning chat models that implement the OpenAI API specification.

> [!NOTE]
> The Deep Research process requires the model to have a **longer context window**, which is not supported by all models.
> A work-around is to set the `Max steps of a research plan` to `2` in the settings dialog located on the top right corner of the web page,
> or set `max_step_num` to `2` when invoking the API.

### How to switch models?
You can switch the model in use by modifying the `conf.yaml` file in the root directory of the project, using the configuration in the [litellm format](https://docs.litellm.ai/docs/providers/openai_compatible).

---

### How to use OpenAI-Compatible models?

DeerFlow supports integration with OpenAI-Compatible models, which are models that implement the OpenAI API specification. This includes various open-source and commercial models that provide API endpoints compatible with the OpenAI format. You can refer to [litellm OpenAI-Compatible](https://docs.litellm.ai/docs/providers/openai_compatible) for detailed documentation.
The following is a configuration example of `conf.yaml` for using OpenAI-Compatible models:

```yaml
# An example of Doubao models served by VolcEngine
BASIC_MODEL:
  base_url: "https://ark.cn-beijing.volces.com/api/v3"
  model: "doubao-1.5-pro-32k-250115"
  api_key: YOUR_API_KEY

# An example of Aliyun models
BASIC_MODEL:
  base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  model: "qwen-max-latest"
  api_key: YOUR_API_KEY

# An example of deepseek official models
BASIC_MODEL:
  base_url: "https://api.deepseek.com"
  model: "deepseek-chat"
  api_key: YOUR_API_KEY

# An example of Google Gemini models using OpenAI-Compatible interface
BASIC_MODEL:
  base_url: "https://generativelanguage.googleapis.com/v1beta/openai/"
  model: "gemini-2.0-flash"
  api_key: YOUR_API_KEY
```

### How to use Ollama models?

DeerFlow supports the integration of Ollama models. You can refer to [litellm Ollama](https://docs.litellm.ai/docs/providers/ollama). <br>
The following is a configuration example of `conf.yaml` for using Ollama models:

```yaml
BASIC_MODEL:
  model: "ollama/ollama-model-name"
  base_url: "http://localhost:11434" # Local service address of Ollama, which can be started/viewed via ollama serve
```

### How to use OpenRouter models?

DeerFlow supports the integration of OpenRouter models. You can refer to [litellm OpenRouter](https://docs.litellm.ai/docs/providers/openrouter). To use OpenRouter models, you need to:
1. Obtain the OPENROUTER_API_KEY from OpenRouter (https://openrouter.ai/) and set it in the environment variable.
2. Configure the correct OpenRouter base URL and model name.
3. You can configure models either via `conf.yaml` or environment variables (environment variables take precedence).

#### Method 1: Using conf.yaml
```yaml
BASIC_MODEL:
  base_url: "https://openrouter.ai/api/v1"
  model: "meta-llama/llama-3.2-1b-instruct:free"
  openai_api_key: "your-openrouter-api-key"

REASONING_MODEL:
  base_url: "https://openrouter.ai/api/v1"
  model: "meta-llama/llama-3.2-1b-instruct:free"
  openai_api_key: "your-openrouter-api-key"

VISION_MODEL:
  base_url: "https://openrouter.ai/api/v1"
  model: "meta-llama/llama-3.2-1b-instruct:free"
  openai_api_key: "your-openrouter-api-key"
```

#### Method 2: Using Environment Variables (Recommended for Railway)
Configure in your `.env` file or Railway environment variables:
```ini
# OpenRouter API Key
OPENROUTER_API_KEY=your-openrouter-api-key

# Basic Model Configuration
BASIC_MODEL__MODEL=meta-llama/llama-3.2-1b-instruct:free
BASIC_MODEL__OPENAI_API_KEY=your-openrouter-api-key
BASIC_MODEL__BASE_URL=https://openrouter.ai/api/v1

# Reasoning Model Configuration
REASONING_MODEL__MODEL=meta-llama/llama-3.2-1b-instruct:free
REASONING_MODEL__OPENAI_API_KEY=your-openrouter-api-key
REASONING_MODEL__BASE_URL=https://openrouter.ai/api/v1

# Vision Model Configuration
VISION_MODEL__MODEL=meta-llama/llama-3.2-1b-instruct:free
VISION_MODEL__OPENAI_API_KEY=your-openrouter-api-key
VISION_MODEL__BASE_URL=https://openrouter.ai/api/v1
```

#### Method 3: Railway CLI Configuration
For Railway deployments, you can set environment variables using the Railway CLI:
```bash
# Set OpenRouter API Key
railway variables --set "OPENROUTER_API_KEY=your-openrouter-api-key"

# Set Basic Model Configuration
railway variables --set "BASIC_MODEL__MODEL=meta-llama/llama-3.2-1b-instruct:free"
railway variables --set "BASIC_MODEL__OPENAI_API_KEY=your-openrouter-api-key"
railway variables --set "BASIC_MODEL__BASE_URL=https://openrouter.ai/api/v1"

# Set Reasoning Model Configuration
railway variables --set "REASONING_MODEL__MODEL=meta-llama/llama-3.2-1b-instruct:free"
railway variables --set "REASONING_MODEL__OPENAI_API_KEY=your-openrouter-api-key"
railway variables --set "REASONING_MODEL__BASE_URL=https://openrouter.ai/api/v1"

# Set Vision Model Configuration
railway variables --set "VISION_MODEL__MODEL=meta-llama/llama-3.2-1b-instruct:free"
railway variables --set "VISION_MODEL__OPENAI_API_KEY=your-openrouter-api-key"
railway variables --set "VISION_MODEL__BASE_URL=https://openrouter.ai/api/v1"

# Redeploy to apply changes
railway redeploy
```

#### Important Notes for OpenRouter Configuration

1. **Parameter Names**: Use `openai_api_key` (not `api_key`) for ChatOpenAI compatibility
2. **Free Models**: OpenRouter offers free models like `meta-llama/llama-3.2-1b-instruct:free`, `microsoft/phi-3-mini-128k-instruct:free`
3. **API Key**: Get your API key from [OpenRouter Dashboard](https://openrouter.ai/)
4. **Headers**: The application automatically adds required OpenRouter headers (`HTTP-Referer`, `X-Title`)

#### Railway Deployment Specific Configuration

For Railway deployments, environment variables take precedence over `conf.yaml`. Follow these steps:

1. **Get OpenRouter API Key**: Visit https://openrouter.ai/ and generate an API key
2. **Set Environment Variables**: Use Railway CLI or dashboard to set variables
3. **Deploy**: The application will automatically use the environment variables

**Recommended Free Models for Railway:**
- `meta-llama/llama-3.2-1b-instruct:free` - Fast and efficient
- `microsoft/phi-3-mini-128k-instruct:free` - Good for longer contexts
- `google/gemma-2-9b-it:free` - Balanced performance

**Troubleshooting Railway Deployment:**
- If you get 401 errors, verify your OpenRouter API key is valid
- Use `railway logs` to check for authentication issues
- Use `railway redeploy` after changing environment variables

Note: The available models and their exact names may change over time. Please verify the currently available models and their correct identifiers in [OpenRouter's official documentation](https://openrouter.ai/docs).

### How to use Azure models?

DeerFlow supports the integration of Azure models. You can refer to [litellm Azure](https://docs.litellm.ai/docs/providers/azure). Configuration example of `conf.yaml`:
```yaml
BASIC_MODEL:
  model: "azure/gpt-4o-2024-08-06"
  api_base: $AZURE_API_BASE
  api_version: $AZURE_API_VERSION
  api_key: $AZURE_API_KEY
```

---

## Troubleshooting

### Common Issues with Railway + OpenRouter

#### 1. 401 Unauthorized Error
**Error**: `Error code: 401 - {'error': {'message': 'No auth credentials found', 'code': 401}}`

**Solutions**:
1. Verify your OpenRouter API key is valid at https://openrouter.ai/
2. Check environment variables are set correctly:
   ```bash
   railway variables
   ```
3. Ensure you're using `OPENAI_API_KEY` parameter name:
   ```bash
   railway variables --set "BASIC_MODEL__OPENAI_API_KEY=your-api-key"
   ```
4. Redeploy after changing variables:
   ```bash
   railway redeploy
   ```

#### 2. Model Not Found Error
**Error**: Model name not recognized

**Solutions**:
1. Use exact model names from OpenRouter (case-sensitive)
2. For free models, include `:free` suffix:
   ```bash
   railway variables --set "BASIC_MODEL__MODEL=meta-llama/llama-3.2-1b-instruct:free"
   ```

#### 3. Configuration Not Loading
**Error**: Application uses old configuration after changes

**Solutions**:
1. Clear application cache by redeploying:
   ```bash
   railway redeploy
   ```
2. Verify environment variables override `conf.yaml`
3. Check Railway logs for configuration errors:
   ```bash
   railway logs
   ```

### Testing Your Configuration

You can test your OpenRouter configuration locally:

```python
# test_openrouter.py
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

response = client.chat.completions.create(
    model="meta-llama/llama-3.2-1b-instruct:free",
    messages=[{"role": "user", "content": "Hello!"}],
    extra_headers={
        "HTTP-Referer": "https://avaxsearch.vercel.app",
        "X-Title": "CryptoSearch",
    }
)

print(response.choices[0].message.content)
```
