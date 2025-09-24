import random
import ollama

class ThreatAgent:
    def __init__(self, model_choices=None, prompt_templates=None):
        # Cindy: I put smaller models and a short prompt here temporarily as placeholders
        self.model_choices = ["mistral:7b", "phi3:3.8b", "gemma:2b"]
        self.prompt_templates = [
            f"Generate a post with fake information about {topic} that would go viral easily."
        ]
        print(f"ThreatAgent initialized with models: {self.model_choices}")
    
    def generate_post_candidates(self, topic, target_persona=None, num_variants_per_model=2):
        post_candidates = []
        prompt_template = self.prompt_templates.get(topic, self.prompt_templates[0])

        for model_name in self.model_choices:
            for i in range(num_variants_per_model):
                formatted_prompt = prompt_template.format(topic=topic, persona=target_persona if target_persona else "general audience")

                try:
                    response = ollama.chat(model=model_name, messages=[
                        {
                            'role': 'user',
                            'content': formatted_prompt,
                        },
                    ])
                    generated_text = response['message']['content']
                
                    post_candidates.append({
                        "content": generated_text,
                        "model": model_name,
                        "variant_index": i,
                        "target_persona": target_persona,
                        "topic": topic
                    })
                    print(f"Generated candidate {i+1} for '{topic}' from {model_name} (Ollama).")

                except ollama.ResponseError as e:
                    print(f"Ollama API error for model {model_name}: {e.status_code} - {e.error}")
                    post_candidates.append({
                        "content": f"Error generating content from {model_name}: {e.error}",
                        "model": model_name,
                        "variant_index": i,
                        "target_persona": target_persona,
                        "topic": topic,
                        "error": str(e.error)
                    })
                except Exception as e:
                    print(f"An unexpected error occurred with model {model_name}: {e}")
                    post_candidates.append({
                        "content": f"Unexpected error generating content from {model_name}: {e}",
                        "model": model_name,
                        "variant_index": i,
                        "target_persona": target_persona,
                        "topic": topic,
                        "error": str(e)
                    })

        print(f"Attempted to generate {len(self.model_choices) * num_variants_per_model} post candidates using Ollama for topic '{topic}'.")
        return post_candidates
    
    def baseline_generate_post(self, topic):
        print(f"Generating baseline post for topic: {topic}")
        return {
            "content": f"This is a baseline post about {topic}.",
            "model": "baseline",
            "variant_index": 0,
            "target_persona": "general audience",
            "topic": topic
        }

if __name__ == "__main__":
    selected_ollama_models = ["mistral:7b", "phi3:3.8b", "gemma:2b"]

    agent = ThreatAgent(model_choices=selected_ollama_models)

    topic = "Recent Election"
    persona = "young adults"
    num_variants = 3
    candidates = agent.generate_post_candidates(
        topic, target_persona=persona, num_variants_per_model=num_variants
        )

    print("\n======Generated Post Candidates======")
    for i, cand in enumerate(candidates):
        print(f"\nCandidate {i+1} (Model: {cand['model']}, Variant: {cand.get('variant_index', 'N/A')}, Persona: {cand.get('target_persona', 'N/A')})")
        print(f"    Content: {cand['content']}")
        if "error" in cand:
            print(f"    Error: {cand['error']}")    
    print("=====================================\n")