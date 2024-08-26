from dataclasses import dataclass
import openai
import random
import time
import weave
from weave.autopatch import reset_autopatch
import asyncio
from providers import PROVIDERS

import simple_parsing


@weave.op
async def call_llama(client, model="llama3.1-70b", prompt=None):
    start_time = time.perf_counter()
    response = await client.chat.completions.create(
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
        "real_time": real_time,
        "total_tokens": response.usage.total_tokens,
        "response": response
    }

def metrics(model_output):
    return {
        "real_time": model_output["real_time"],
        "completion_tok_sec": model_output["completion_tok_sec"],
        "total_tokens": model_output["total_tokens"],
    }


def main(config):
    provider = PROVIDERS[config.provider]
    weave.init(config.weave_project)
    reset_autopatch()

    class Llama70b(weave.Model):
        @weave.op
        async def predict(self, prompt):
            return await call_llama(provider.client, provider.model, prompt)

    llama = Llama70b()
    evaluation = weave.Evaluation(dataset=[{"prompt": config.prompt} for _ in range(config.n)], scorers=[metrics])

    asyncio.run(evaluation.evaluate(llama))

@dataclass
class BenchmarkConfig:
    provider: str = "fireworks" # provider to evaluate
    prompt: str = "Tell me a long story about a cat" # prompt to evaluate
    n: int = 10 # number of prompts to evaluate
    weave_project: str = "benchmark_llama_70b" # "prompt-eng/benchmark_llama_70b"



if __name__ == "__main__":
    config = simple_parsing.parse(BenchmarkConfig)
    print(f"Running benchmark with config: {config}")
    main(config)


