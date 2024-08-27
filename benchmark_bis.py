from dataclasses import dataclass
import openai
import random
import time
import asyncio
from tqdm import tqdm
import simple_parsing

from providers import PROVIDERS

def call_llama(client, model="llama3.1-70b", prompt=None):
    start_time = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        max_tokens=2048,
        temperature=random.random(),
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    end_time = time.perf_counter()
    real_time = end_time - start_time
    completion_tok_sec = response.usage.completion_tokens / real_time

    return {
        "real_time": real_time, 
        "completion_tok_sec": completion_tok_sec, 
        "response": response
    }


def evaluate_model_perf(client, model, prompt, num_runs=10):
    perf_results = {
        "real_time": 0., 
        "completion_tok_sec": 0., 
    }
    for i in tqdm(range(num_runs)):
        output = call_llama(client, model=model, prompt=prompt)
        perf_results["real_time"] += output["real_time"]
        perf_results["completion_tok_sec"] += output["completion_tok_sec"]
    # compute averages
    perf_results["real_time"] /= num_runs
    perf_results["completion_tok_sec"] /= num_runs
    return perf_results


def main(config):
    provider = PROVIDERS[config.provider]

    perf_results = evaluate_model_perf(provider.client, provider.model, config.prompt, config.n)
    print(perf_results)

    


@dataclass
class BenchmarkConfig:
    provider: str = "fireworks" # provider to evaluate
    prompt: str = "Tell me a long story about a cat" # prompt to evaluate
    n: int = 10 # number of prompts to evaluate
    use_weave: bool = False # whether to use weave to evaluate the model



if __name__ == "__main__":
    config = simple_parsing.parse(BenchmarkConfig)
    print(f"Running benchmark with config: {config}")
    
    if config.use_weave:
        import weave
        weave.init("overhead")
    main(config)


