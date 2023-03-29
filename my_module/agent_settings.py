class AgentSettings:
    def __init__(self, system_prompt, filename_prefix = "agent", gpt_max_reply_tokens = 500, max_session_memory = 2500, gpt_temperature = 1.0, gpt_max_total_tokens = 4096):
        self.gpt_max_reply_tokens = gpt_max_reply_tokens
        self.gpt_max_total_tokens = gpt_max_total_tokens
        self.gpt_temperature = gpt_temperature
        self.system_prompt = system_prompt
        self.filename_prefix = filename_prefix
        self.max_session_memory = max_session_memory

