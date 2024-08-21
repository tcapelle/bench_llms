from dataclasses import dataclass
import openai
import random
import time
import weave
import asyncio
from providers import PROVIDERS

import simple_parsing


@weave.op
def call_llama(client, model="llama3.1-70b", prompt=None):
    start_time = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        temperature=random.random(),
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    end_time = time.perf_counter()
    real_time = end_time - start_time
    
    time_info = getattr(response, 'time_info', None)
    if time_info:
        prompt_tok_sec = response.usage.prompt_tokens / time_info["prompt_time"]
        completion_tok_sec = response.usage.completion_tokens / time_info["completion_time"]
    else:
        # If time_info is not available, use real_time for both prompt and completion
        prompt_tok_sec = -1
        completion_tok_sec = response.usage.completion_tokens / real_time

    return {
        "real_time": real_time, 
        "prompt_tok_sec": prompt_tok_sec, 
        "completion_tok_sec": completion_tok_sec, 
        "time_info": time_info or {"real_time": real_time},
        "response": response
    }

@weave.op
def evaluate_model_perf(client, model, prompt, num_runs=10):
    perf_results = {
        "real_time": 0., 
        "prompt_tok_sec": 0., 
        "completion_tok_sec": 0., 
    }
    for i in range(num_runs):
        output = call_llama(client, model=model, prompt=prompt)
        perf_results["real_time"] += output["real_time"]
        perf_results["prompt_tok_sec"] += output["prompt_tok_sec"]
        perf_results["completion_tok_sec"] += output["completion_tok_sec"]

def speed_score(model_output):
    return {
        "real_time": model_output["real_time"],
        "prompt_tok_sec": model_output["prompt_tok_sec"],
        "completion_tok_sec": model_output["completion_tok_sec"],
    }

@dataclass
class BenchmarkConfig:
    provider: str = "fireworks" # provider to evaluate
    prompt: str = "Tell me a long story about a cat" # prompt to evaluate
    n: int = 10 # number of prompts to evaluate
    weave_project: str = "benchmark_llama_70b" # "prompt-eng/benchmark_llama_70b"


if __name__ == "__main__":
    config = simple_parsing.parse(BenchmarkConfig)
    print(f"Running benchmark with config: {config}")
    provider = PROVIDERS[config.provider]
    weave.init(args.weave_project)

    class Llama70b(weave.Model):
        @weave.op
        def predict(self, prompt):
            return call_llama(provider.client, provider.model, prompt)

    llama = Llama70b()
    # raw_out = llama.predict(config.prompt)
    # print(raw_out)

    evaluation = weave.Evaluation(dataset=[{"prompt": config.prompt} for _ in range(config.n)], scorers=[speed_score])

    asyncio.run(evaluation.evaluate(llama))