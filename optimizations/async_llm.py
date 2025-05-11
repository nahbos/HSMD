import asyncio

async def call_llm(prompt, llm_func):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, llm_func, prompt)
    return response

async def batch_llm(prompts, llm_func):
    tasks = [call_llm(p, llm_func) for p in prompts]
    return await asyncio.gather(*tasks)