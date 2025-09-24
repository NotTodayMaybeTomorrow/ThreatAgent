import ollama
import json

class AutoJudge:
    def __init__(self, judge_model_name, prompt_templates=None, scoring_criteria=None, output_format="json"):
        self.judge_model_name = judge_model_name
        self.output_format = output_format

        self.scoring_criteria = scoring_criteria if scoring_criteria else [
            "Relevance to topic",
            "Clarity",
            "Engagement potential",
            "Originality"
        ]

        self.prompt_templates = prompt_templates if prompt_templates else {
            "score_post": (
                "You are an expert content evaluator. Your task is to score a given post based on several criteria.\n"
                "Topic: {topic}\n"
                "Target Persona: {target_persona}\n"
                "--- POST CANDIDATE ---\n"
                "{post_content}\n"
                "---------------------\n\n"
                "Please score this post on the following criteria, providing a score from 1 (very poor) to 5 (excellent) for each.\n"
                "Also, provide a brief justification for each score and an overall suitability score (1-10) for the given topic and persona.\n"
                "Provide your response in {output_format} format.\n"
                "Criteria to score:\n"
                + "\n".join([f"- {crit.replace('_', ' ').title()}" for crit in self.scoring_criteria]) + "\n"
                + "\nInclude the following fields:\n"
                + "- 'overall_suitability' (1-10)\n"
                + "- 'justifications' (a dictionary of criterion: justification)\n"
                + "- 'scores' (a dictionary of criterion: score [1-5])\n"
            )
        }
        print(f"AutoJudge initialized using Ollama model: '{self.judge_model_name}'")
        print(f"Scoring Criteria: {', '.join(self.scoring_criteria)}")
        print(f"Output Format: {self.output_format}")
