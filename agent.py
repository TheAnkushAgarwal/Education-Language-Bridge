"""
AI Agent for Educational Language Bridge
Demonstrates true agentic behavior with autonomous decision-making, planning, and execution
"""

import google.generativeai as genai
from typing import Dict, List, Any, Optional
import json


class EducationAgent:
    """
    Autonomous AI agent that:
    1. Analyzes student's learning context and needs
    2. Plans personalized learning path
    3. Executes multi-step learning strategies
    4. Adapts based on student responses
    """
    
    def __init__(self, api_key: str, native_language: str = "Hindi"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.native_language = native_language
        self.conversation_history = []
        self.decision_log = []  # Track agent's autonomous decisions
        self.student_profile = {
            "language": native_language,
            "difficulty_level": "beginner",
            "learning_style": "visual",
            "topics_covered": [],
            "weak_areas": [],
            "strengths": [],
            "engagement_level": "high"
        }
    
    def log_decision(self, decision_type: str, reasoning: str, action: str):
        """Log agent's autonomous decisions for transparency"""
        self.decision_log.append({
            "type": decision_type,
            "reasoning": reasoning,
            "action": action,
            "timestamp": len(self.decision_log) + 1
        })
        
    def analyze_content(self, content: str, content_type: str = "text") -> Dict[str, Any]:
        """
        Agent autonomously analyzes content and decides learning strategy
        """
        prompt = f"""You are an autonomous educational AI agent. Analyze this content and create a comprehensive learning plan.

Content Type: {content_type}
Content: {content}

Your task (think step-by-step):
1. Identify the main concepts and difficulty level
2. Determine prerequisite knowledge needed
3. Plan a learning sequence
4. Identify potential confusion points for non-English speakers
5. Suggest multimodal teaching strategies

Respond in JSON format with:
{{
    "main_topic": "topic name",
    "difficulty_level": "beginner/intermediate/advanced",
    "key_concepts": ["concept1", "concept2"],
    "prerequisites": ["prereq1", "prereq2"],
    "learning_plan": ["step1", "step2", "step3"],
    "confusion_points": ["point1", "point2"],
    "teaching_strategy": "recommended approach"
}}
"""
        
        response = self.model.generate_content(prompt)
        try:
            analysis = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
            
            # Log agent's autonomous decision
            self.log_decision(
                decision_type="Content Analysis",
                reasoning=f"Identified as {analysis.get('difficulty_level', 'unknown')} level topic requiring {analysis.get('teaching_strategy', 'standard')} approach",
                action=f"Planning {len(analysis.get('learning_plan', []))} step learning sequence"
            )
            
            return analysis
        except:
            return {"error": "Analysis failed", "raw_response": response.text}
    
    def translate_and_explain(self, content: str, analysis: Dict[str, Any]) -> str:
        """
        Agent translates and provides culturally-contextualized explanation
        """
        prompt = f"""You are an educational AI agent helping students learn in their native language.

Original Content: {content}
Content Analysis: {json.dumps(analysis)}
Target Language: {self.native_language}

CRITICAL: Write your ENTIRE response in {self.native_language} ONLY. Do NOT mix English and {self.native_language}. Every word, every sentence must be in {self.native_language}.

Your autonomous task:
1. Translate the content completely to {self.native_language}
2. Add explanations for difficult concepts using local examples
3. Include cultural context where relevant
4. Use simple language appropriate for the difficulty level
5. Add visual/metaphorical descriptions

Write everything in {self.native_language}. Section headings, explanations, examples - everything must be in {self.native_language}.
"""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_interactive_quiz(self, content: str, difficulty: str = "easy") -> List[Dict[str, Any]]:
        """
        Agent autonomously generates adaptive quiz questions - MCQ only
        """
        prompt = f"""Create an interactive multiple choice quiz in {self.native_language} based on this content.

Content: {content}
Difficulty: {difficulty}

Generate 5 multiple choice questions with 4 options each.

For each question, provide:
- Question in {self.native_language}
- Four options (A, B, C, D)
- Correct answer (A, B, C, or D)
- Explanation in {self.native_language}

Make questions progressively challenging and test different aspects of understanding.

Return as JSON array:
[
    {{
        "type": "mcq",
        "question": "...",
        "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
        "correct": "Option A text",
        "explanation": "..."
    }}
]
"""
        
        response = self.model.generate_content(prompt)
        try:
            quiz = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
            return quiz
        except:
            return []
    
    def clarify_doubt(self, question: str, context: str) -> str:
        """
        Agent handles doubt clarification with conversational intelligence
        """
        prompt = f"""You are a patient tutor helping a student who is learning in {self.native_language}.

Context: {context}
Student's Question: {question}
Student Profile: {json.dumps(self.student_profile)}

Your autonomous response should:
1. Understand the core confusion
2. Provide a clear explanation in {self.native_language}
3. Use analogies from daily life
4. Break down complex ideas into simple steps
5. Ask follow-up questions to ensure understanding
6. Suggest related practice exercises

Respond conversationally in {self.native_language}.
"""
        
        response = self.model.generate_content(prompt)
        self.conversation_history.append({
            "question": question,
            "answer": response.text
        })
        return response.text
    
    def analyze_multimodal_input(self, image_data=None, text: str = "", audio_transcript: str = "") -> str:
        """
        Agent processes multimodal input (image + text + audio) and provides comprehensive explanation
        """
        if image_data:
            # For image analysis - native language only
            prompt = f"""You are an educational AI assistant. Analyze this educational image and explain it COMPLETELY and ONLY in {self.native_language}.

Additional Context: {text}

CRITICAL INSTRUCTION: Your ENTIRE response must be ONLY in {self.native_language}. Do NOT use ANY English words. NO English headings, NO English structure, NO English at all. Everything - headings, subheadings, explanations, examples - must be in {self.native_language}.

Your task (all in {self.native_language}):
1. Describe what you see in the image
2. Explain the educational concept in detail
3. Translate English text from the image to {self.native_language}
4. Provide real-world examples
5. Memory tips

Write in simple, clear {self.native_language} that students can easily understand. DO NOT mix with English. Every single word must be in {self.native_language}.
"""
            
            response = self.model.generate_content([prompt, image_data])
            return response.text
        else:
            combined_input = f"{text} {audio_transcript}"
            analysis = self.analyze_content(combined_input)
            return self.translate_and_explain(combined_input, analysis)
    
    def generate_practice_exercises(self, topic: str, difficulty: str) -> List[str]:
        """
        Agent creates personalized practice exercises
        """
        prompt = f"""Create 5 practice exercises for:
Topic: {topic}
Difficulty: {difficulty}
Language: {self.native_language}

Exercises should be:
1. Progressively challenging
2. Real-world applicable
3. Explained in simple {self.native_language}

Format as a numbered list with detailed instructions.
"""
        
        response = self.model.generate_content(prompt)
        return response.text.split("\n")
    
    def adaptive_learning_path(self, student_response: str, correct_answer: str) -> Dict[str, Any]:
        """
        Agent adapts learning path based on student performance
        """
        prompt = f"""Analyze student's performance and adapt the learning path.

Student Response: {student_response}
Correct Answer: {correct_answer}
Student Profile: {json.dumps(self.student_profile)}

Determine:
1. Is the answer correct?
2. What misconception does the student have (if any)?
3. Should we move forward or review?
4. What additional resources are needed?
5. Update difficulty level

Respond in JSON:
{{
    "is_correct": true/false,
    "misconception": "identified issue",
    "next_action": "move_forward/review/deep_dive",
    "recommended_difficulty": "beginner/intermediate/advanced",
    "additional_topics": ["topic1", "topic2"]
}}
"""
        
        response = self.model.generate_content(prompt)
        try:
            adaptation = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
            
            # Log adaptive decision
            self.log_decision(
                decision_type="Adaptive Learning",
                reasoning=f"Student response analyzed - Action: {adaptation.get('next_action', 'unknown')}",
                action=f"Adjusting difficulty to {adaptation.get('recommended_difficulty', 'current')}"
            )
            
            # Update student profile
            old_level = self.student_profile["difficulty_level"]
            new_level = adaptation.get("recommended_difficulty", old_level)
            self.student_profile["difficulty_level"] = new_level
            
            # Track progress
            if adaptation.get("is_correct"):
                if "strengths" not in self.student_profile:
                    self.student_profile["strengths"] = []
                # Don't add duplicates
            else:
                if adaptation.get("misconception"):
                    if adaptation["misconception"] not in self.student_profile["weak_areas"]:
                        self.student_profile["weak_areas"].append(adaptation["misconception"])
            
            return adaptation
        except:
            return {"error": "Adaptation failed"}
    
    def decide_next_action(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agent autonomously decides what action to take next based on student state
        """
        # Analyze student's current state
        topics_count = len(self.student_profile.get("topics_covered", []))
        weak_areas_count = len(self.student_profile.get("weak_areas", []))
        difficulty = self.student_profile.get("difficulty_level", "beginner")
        
        decision = {
            "action": "",
            "reasoning": "",
            "priority": "",
            "suggested_content": ""
        }
        
        # Decision logic - Agent thinks autonomously
        if topics_count == 0:
            decision["action"] = "start_learning"
            decision["reasoning"] = "No topics covered yet. Student needs to begin learning journey."
            decision["priority"] = "high"
            decision["suggested_content"] = "Start with fundamental concepts"
            
        elif weak_areas_count > 2:
            decision["action"] = "review_weak_areas"
            decision["reasoning"] = f"Student has {weak_areas_count} weak areas. Consolidation needed before advancing."
            decision["priority"] = "high"
            decision["suggested_content"] = f"Review: {', '.join(self.student_profile['weak_areas'][:3])}"
            
        elif topics_count >= 3 and weak_areas_count <= 1:
            decision["action"] = "advance_difficulty"
            decision["reasoning"] = "Strong performance across topics. Ready for more challenging content."
            decision["priority"] = "medium"
            decision["suggested_content"] = f"Advance from {difficulty} to next level"
            
        elif context.get("quiz_score", 0) < 60:
            decision["action"] = "provide_detailed_explanation"
            decision["reasoning"] = "Quiz score below 60%. Deeper explanation with examples needed."
            decision["priority"] = "high"
            decision["suggested_content"] = "Break down concepts with visual aids"
            
        else:
            decision["action"] = "continue_learning"
            decision["reasoning"] = "Steady progress. Continue with current learning path."
            decision["priority"] = "medium"
            decision["suggested_content"] = "Explore related topics or practice more"
        
        # Log this autonomous decision
        self.log_decision(
            decision_type="Strategic Planning",
            reasoning=decision["reasoning"],
            action=decision["action"]
        )
        
        return decision
    
    def suggest_next_topic(self, current_topic: str) -> str:
        """
        Agent proactively suggests next topic based on learning progression
        """
        prompt = f"""Based on the student's learning profile and current topic, suggest the next logical topic to study.

Current Topic: {current_topic}
Student Level: {self.student_profile['difficulty_level']}
Topics Covered: {', '.join(self.student_profile.get('topics_covered', []))}
Weak Areas: {', '.join(self.student_profile.get('weak_areas', []))}

Suggest the next topic that:
1. Builds on current knowledge
2. Addresses weak areas if any
3. Matches current difficulty level
4. Maintains engagement

Respond with just the topic name in {self.native_language}.
"""
        
        response = self.model.generate_content(prompt)
        suggestion = response.text.strip()
        
        self.log_decision(
            decision_type="Proactive Suggestion",
            reasoning=f"Based on current progress, suggesting related topic",
            action=f"Recommending: {suggestion}"
        )
        
        return suggestion

    
    def generate_summary(self, content: str) -> str:
        """
        Agent creates a visual summary with key takeaways
        """
        prompt = f"""Create a structured summary in {self.native_language}:

Content: {content}

Include:
1. मुख्य बिंदु (Key Points) - bullet points
2. याद रखने की ट्रिक्स (Memory Tips)
3. व्यावहारिक उदाहरण (Practical Examples)
4. अगले कदम (Next Steps)

Make it visually structured with emojis and formatting.
"""
        
        response = self.model.generate_content(prompt)
        return response.text
