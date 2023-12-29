# Evaluating LLM Performance on General Program Analysis

## File Structure

- **data:** Contains all our datasets.
- **results:** Contains results for open-source models.
    - For example: `results/llama/CD_prompt_template_1/example_0.txt` contains the prompt 1 and llama model's response for first sample for Cyclic Dependency(CD).
- **scripts:** Contains all Python scripts required to load and run the models.

## How to Run the Artifact

To run the artifact, use the following command:

```bash
python main.py --model "Model_name" --dataset "dataset_name" --template "Prompt_template" --mode "Mode_name"

-**Model_name**: Choose from: gpt-3.5-turbo, llama, llama7, starcoder, wizardcoder, falcon (You have to choose these exact names)
-**dataset_name**: Choose from: CFG, CD, DFG, pointer.
-**Prompt_template**: Choose from: 1, 2, 3.
-**Mode_name**: Choose from: CFG, CD, DFG, pointer.

For example, to run model CodeLlama with 34 billion parameter model, with pointer dataset and prompt 3, we need to run

python main.py --model llama --dataset pointer --template 3 --mode pointer

**(llama7 is for 7 billion model)

We have also included an image file (Run.png) which shows how to load and run a model in a proper envrionment. If you face any problems regarding running our artifact, please contact with us.

## GPU requirement
** To run all these model's (except gpt 3.5), we need GPU with at least 30GB+ memory. Otherwise, the models can not be loaded.
** Colab's paid version may be an option to run the script with powerful gpu.

##Clarifaction
** For commercial models(GPT, BARD, CLAUDE), we have used the web interface for response genration, because either the APIs are too costly for these models or the models are not available for free use.