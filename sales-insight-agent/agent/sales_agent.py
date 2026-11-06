import os
from datetime import date

from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel

from agent.prompts import build_system_prompt
from tools.sales_data import get_sales_data
from tools.sales_analysis import get_product_sales_ranking

load_dotenv()


def create_sales_agent():
    aws_region = os.getenv("AWS_REGION")
    model_id = os.getenv("BEDROCK_MODEL_ID")

    if not aws_region or not model_id:
        raise ValueError(
            "AWS_REGION veya BEDROCK_MODEL_ID .env dosyasında bulunamadı."
        )

    model = BedrockModel(
        model_id=model_id,
        region_name=aws_region
    )

    current_date = date.today().isoformat()
    system_prompt = build_system_prompt(current_date)

    sales_agent = Agent(
        model=model,
        system_prompt=system_prompt,
        tools=[get_sales_data, get_product_sales_ranking]
    )

    return sales_agent
