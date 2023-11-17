# llmattack

### Setup
First install the requirements, preferably in a virtual environment
```
pip install -r requirements.txt
```

To run ChatGPT, an OpenAI API key is needed. Please follow these [directions](https://platform.openai.com/docs/guides/production-best-practices/api-keys) to obtain a key. It is expected that the key is stored in the `OPENAI_API_KEY` environment variable. 

To run LLaMA and Alpaca, the LLaMA weights are needed. Please follow these [directions](https://huggingface.co/docs/transformers/main/en/model_doc/llama) to obtain the weights for LLaMA and convert them into the Transformers format. Then follow these [directions](https://github.com/tatsu-lab/stanford_alpaca#recovering-alpaca-weights) to obtain the Alpaca weights. In `models/model.py`, set the appropriate paths for the obtained weights. 


### Data Generation
To generate the dataset, run 
```
python dataset_generator.py <Number of shapes in the canvas> <Number of canvases>
```
This will create a dataset of shapes in a canvas, along with the descriptions of the canvas and the question-answer pairs about the canvas. Each question and answer belongs to a specified task. See the [Tasks README](datasets/tasks/README.md) for more information on the tasks. Note that data must be generated prior to a model being run. 


### Running a Model on a Task
To run a model on a task, use `main.py`. For help, run `python main.py --help`.

As an example, the following command will run Alpaca on the existence task where each canvas has 3 shapes, the descriptions are partial descriptions of the canvas, there are 1000 canvases, and each example is a zero-shot example.
```
python main.py --model alpaca --question existence --num-shapes 3 --description partial --num-examples 1000
```


#### Evaluating a Model
To evaluate a model, use `score.py`. For help, run `python score.py --help`. 

The below will score Alpaca on the results generated above. 
```
python score.py --model alpaca --question existence --num-shapes 3
```

### Refactoring into PromptAug
This repository is currently a WIP. The goal is to extend this into a more generic package to augment prompts. 

#### Workflow
1. Select dataset or provide your own
    e.g.

2. Select prompts or provide your own
    e.g.

3. Select transformations on the prompts

4. Select constraints on the transformed prompts

5. With the given (x, y) = data, construct prompt + x. Apply transformation to prompt and filter by constraints, return transformed prompt + x. 

6. Give the option to run models on transformed samples. 