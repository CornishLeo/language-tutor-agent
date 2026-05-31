from pydantic import BaseModel, Field

class GrammarCriticSchema(BaseModel):
    is_correct: bool = Field(
        description="A boolean value representing whether the users input is correct or not."
    )

    correction: str = Field(
        description="A corrected version of the users input purely in Japanese. Leave blank if it was already correct."
    )

    explanation: str = Field(
        description="An explanation of why the users input was wrong in English. Leave blank if it was already correct."
    )