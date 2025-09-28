import os
from dotenv import load_dotenv
from typing import Dict
import json

from openai import OpenAI

import opik
from opik import track
from opik.integrations.openai import track_openai
from opik.evaluation import evaluate
from opik.evaluation.metrics import (
    Hallucination,
    AnswerRelevance,
    ContextPrecision,
    ContextRecall
)

opik.configure(use_local=True) # Or True if running Opik locally

load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL=os.getenv("OPENAI_BASE_URL")

monitoring = os.getenv("ENABLE_MONITORING")

client = OpenAI(
    api_key=OPENAI_API_KEY,  # this is also the default, it can be omitted
    base_url=OPENAI_BASE_URL
    )

if monitoring == "Yes":
    tracked_client = track_openai(client)
else:
    tracked_client = client


opik_client=opik.Opik()

hallucination_metric = Hallucination()
answer_relevance_metric = AnswerRelevance()
context_precision_metric = ContextPrecision()
context_recall_metric = ContextRecall() 


async def build_prompt(input:str):
    prompt_template = """
    You understand the decline codes and special decline conditions and limits and fault errors from the 
    popular schemes such as VISA, Mastercard, Amex, Discover, JCB, UnionPay, Maestro, Electron, etc.
    The answer should contain a clear description of the decline code and reason. And the answer should be a line. 
    
    Decline Code: {code}
    Reason: {reason}

    """.strip()

    input_json = json.loads(input)
    prompt = prompt_template.format(code=input_json['code'], reason=input_json['reason']).strip()
    return prompt


async def respond_with_llm(prompt, model="gpt-4o-mini"):
    response = tracked_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

@track
def my_llm_application(input:str)->str:
    prompt = build_prompt(input)
    print("Prompt :", prompt)

    llm_response =  respond_with_llm(prompt)
    print("LLM Response :", llm_response,"\n\n" )
    return str(llm_response)


def evaluation_task(x:Dict):
    return {
        "output": my_llm_application(x['input'])
    }


def prepare_data():
    with open("dataset.json", "r") as f:
        inputs = json.load(f)

    dataset_name="payments_eval"
    dataset=opik_client.get_or_create_dataset(dataset_name) 
    dataset.insert(inputs)
    return dataset


def main(dataset):
    evaluation = evaluate(
        dataset=dataset,
        task=evaluation_task,
        scoring_metrics=[hallucination_metric, answer_relevance_metric, context_precision_metric, context_recall_metric],
        experiment_config={
            "model":"gpt-4o-mini"
        }
    )

if __name__== "__main__":
    dataset = prepare_data()
    main(dataset)