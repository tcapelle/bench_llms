# LLM Benchmark Tool

This tool benchmarks the performance of various Large Language Models (LLMs) across different providers.

## Features

- Supports multiple LLM providers (Octo, Groq, Fireworks, Together)
- Measures real-time performance, prompt tokens per second, and completion tokens per second
- Configurable number of runs and custom prompts
- Uses Weave for evaluation and scoring

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/llm-benchmark-tool.git
   cd llm-benchmark-tool
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables for API keys:
   ```
   export OCTO_API_KEY=your_octo_api_key
   export GROQ_API_KEY=your_groq_api_key
   export FIREWORKS_API_KEY=your_fireworks_api_key
   export CEREBRAS_API_KEY=your_cerebras_api_key
   export TOGETHER_API_KEY=your_together_api_key
   ```

## Usage

Run the benchmark with default settings:

```
python benchmark.py
```

Customize the benchmark:

```
python benchmark.py --provider fireworks --prompt "Explain quantum computing" --n 5
```

## Project Structure

- `benchmark.py`: Main script for running the benchmark
- `providers.py`: Definitions of LLM providers
- `requirements.txt`: List of Python dependencies
- `README.md`: This file

## Adding a New Provider

To add a new LLM provider to the benchmark tool, follow these steps:

1. Open the `providers.py` file.

2. Add a new entry to the `PROVIDERS` dictionary with the following format:

   ```python
   "provider_name": Provider(
       client=openai.OpenAI(
           base_url="https://api.provider.com/v1",
           api_key=os.environ.get("PROVIDER_API_KEY")
       ),
       model="provider-model-name"
   )
   ```

   Replace `provider_name`, `https://api.provider.com/v1`, `PROVIDER_API_KEY`, and `provider-model-name` with the appropriate values for the new provider.

3. Add the new provider's API key to your environment variables:

   ```
   export PROVIDER_API_KEY=your_provider_api_key
   ```

4. Update the README to include the new provider in the list of supported providers and add the new environment variable to the setup instructions.

5. Test the new provider by running the benchmark with the new provider name:

   ```
   python benchmark.py --provider provider_name
   ```

Remember to ensure that the new provider's API is compatible with the OpenAI client format used in this tool. If it's not, you may need to modify the `call_llama` function in `benchmark.py` to handle any differences in the API structure.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.