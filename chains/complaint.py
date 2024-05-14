import base64
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import HumanMessage
from langchain_core.utils.json import parse_json_markdown

from prompts.complaint import COMPLAINT_PROMPT


def load_image(image_path: str) -> dict:
    """Load image from file and encode it as base64."""
    image_path = image_path

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    image_base64 = encode_image(image_path)
    return {"image": image_base64}


class ImageInformation(BaseModel):
    """Information about an image."""

    image_description: str = Field(description="a short description of the image")
    is_complaint_genuine: bool = Field(description="Is the complaint genuine")
    count: int = Field(description="Count of images")


class ComplaintChain:

    def __init__(self) -> None:
        self.parser = JsonOutputParser(pydantic_object=ImageInformation)

    def process_prompt(self, llm, prompt, img, ref):
        img = base64.b64encode(img).decode("utf-8")
        ref = base64.b64encode(ref).decode("utf-8")
        result = llm.invoke(
            [
                HumanMessage(
                    content=[
                        {"type": "text", "text": COMPLAINT_PROMPT.format(input=prompt)},
                        {"type": "text", "text": self.parser.get_format_instructions()},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{img}"},
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{ref}"},
                        },
                    ]
                )
            ]
        )

        return parse_json_markdown(result.content)
