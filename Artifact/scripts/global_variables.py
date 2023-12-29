data_dir = "../data"
result_dir = "../results"

models_ids = {
    "gpt3.5": "gpt-3.5-turbo",
    "llama": "codellama/CodeLlama-34b-Instruct-hf",
    "llama7": "codellama/CodeLlama-7b-Instruct-hf",
    "starcoder": "HuggingFaceH4/starchat-beta",
    "wizardcoder": "WizardLM/WizardCoder-15B-V1.0",
    "falcon":"tiiuae/falcon-40b",
}
api_types = {
    "gpt3.5": "openai",
    "llama": "llama",
    "llama7": "llama",
    "starcoder": "starcoder",
    "wizardcoder": "wizardcoder",
    "hf": "hf",
    "falcon":"falcon",
}
