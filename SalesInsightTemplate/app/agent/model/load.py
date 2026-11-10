from strands.models.bedrock import BedrockModel


def load_model() -> BedrockModel:
    """Load Amazon Nova Micro through Amazon Bedrock."""

    return BedrockModel(
        model_id="eu.amazon.nova-micro-v1:0",
        region_name="eu-west-1"
    )
