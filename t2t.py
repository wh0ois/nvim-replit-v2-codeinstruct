import pynvim
import os
from dataclasses import dataclass, asdict
from ctransformers import AutoModelForCausalLM, AutoConfig


@dataclass
class GenerationConfig:
    temperature: float
    top_k: int
    top_p: float
    repetition_penalty: float
    max_new_tokens: int
    seed: int
    reset: bool
    stream: bool
    threads: int
    stop: list[str]


def format_prompt(user_prompt: str):
    return f"""### Instruction:
{user_prompt}

### Response:"""


def generate(
    llm: AutoModelForCausalLM,
    generation_config: GenerationConfig,
    user_prompt: str,
):
    """run model inference, will return a Generator if streaming is true"""

    return llm(
        format_prompt(
            user_prompt,
        ),
        **asdict(generation_config),
    )

config = AutoConfig.from_pretrained(
    os.path.abspath("/home/models"),
    context_length=2048,
)
llm = AutoModelForCausalLM.from_pretrained(
    os.path.abspath("/home/models/replit-v2-codeinstruct-3b.q4_1.bin"),
    model_type="replit",
    config=config,
)

generation_config = GenerationConfig(
    temperature=0.2,
    top_k=50,
    top_p=0.9,
    repetition_penalty=1.0,
    max_new_tokens=512,  # adjust as needed
    seed=42,
    reset=True,  # reset history (cache)
    stream=True,  # streaming per word/token
    threads=int(os.cpu_count() / 6),  # adjust for your CPU
    stop=["<|endoftext|>"],
)

user_prefix = "[user]: "
assistant_prefix = f"[assistant]:"


@pynvim.plugin
class T2T:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command("T2T", nargs="*", range="")
    def t2t_handler(self, args, range):
        if not args:
            self.nvim.err_write("Error: No arguments provided\n")
            return

        user_input = " ".join(args)
        generator = generate(llm, generation_config, f"{user_prefix}{user_input}")
        response = ""
        for word in generator:
            response += word

        response = response.replace(user_prefix, "").replace(assistant_prefix, "").strip()
        self.nvim.current.buffer.append(response.splitlines())



