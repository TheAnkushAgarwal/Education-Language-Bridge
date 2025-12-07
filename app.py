"""
Education Language Bridge - Multimodal AI Learning Assistant
Demonstrates True Agentic Behavior for Hackathon
"""

import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import io
import base64
from agent import EducationAgent
import pypdf

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Education Language Bridge 🌉",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    .agent-thinking {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'current_content' not in st.session_state:
    st.session_state.current_content = ""
if 'analysis' not in st.session_state:
    st.session_state.analysis = None
if 'quiz' not in st.session_state:
    st.session_state.quiz = []
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = []
if 'topics_learned' not in st.session_state:
    st.session_state.topics_learned = []

def initialize_agent(api_key: str, language: str):
    """Initialize the AI agent"""
    try:
        st.session_state.agent = EducationAgent(api_key, language)
        return True
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        return False

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error extracting PDF text: {str(e)}")
        return ""

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌉 Education Language Bridge</h1>
        <p>AI-Powered Multimodal Learning Assistant with True Agentic Behavior</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        api_key = st.text_input(
            "Google API Key",
            type="password",
            value=os.getenv("GOOGLE_API_KEY", ""),
            help="Enter your Gemini API key"
        )
        
        native_language = st.selectbox(
            "Your Native Language",
            ["Hindi", "Bengali"],
            help="Select your preferred learning language"
        )
        
        if st.button("🚀 Initialize AI Agent", type="primary"):
            if api_key:
                if initialize_agent(api_key, native_language):
                    st.success(f"✅ Agent initialized for {native_language}")
            else:
                st.error("Please enter an API key")
        
        st.divider()
        
        st.header("🤖 Agent Status")
        if st.session_state.agent:
            st.success("🟢 Agent Active")
            st.info(f"**Language:** {st.session_state.agent.native_language}")
            st.info(f"**Level:** {st.session_state.agent.student_profile['difficulty_level']}")
            
            # Show Agent's Decision Log
            if st.session_state.agent.decision_log:
                with st.expander("🧠 Agent Decision Log", expanded=False):
                    st.caption("See the agent's autonomous reasoning")
                    for decision in st.session_state.agent.decision_log[-5:]:  # Show last 5
                        st.markdown(f"""
                        **{decision['type']}**  
                        💭 Reasoning: {decision['reasoning']}  
                        ⚡ Action: {decision['action']}
                        """)
                        st.divider()
        else:
            st.warning("🔴 Agent Not Initialized")
        
        st.divider()
        
        st.header("📊 Features")
        st.markdown("""
        - 🖼️ Image Analysis
        - 📄 PDF Processing
        - 💬 Doubt Clarification
        - 📝 Quiz Generation
        - 🎯 Adaptive Learning
        - 🔄 Real-time Translation
        - 📊 Progress Tracking
        """)
    
    # Main content area
    if not st.session_state.agent:
        st.warning("⚠️ Please initialize the AI agent from the sidebar to begin learning")
        
        # Show demo features
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="feature-box">
                <h3>🎯 Agentic Behavior</h3>
                <p>AI autonomously plans learning paths, adapts difficulty, and provides personalized explanations</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-box">
                <h3>🌍 Multimodal Input</h3>
                <p>Process images, PDFs, text, and audio for comprehensive learning</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-box">
                <h3>🗣️ Native Language</h3>
                <p>Learn complex topics in your mother tongue with cultural context</p>
            </div>
            """, unsafe_allow_html=True)
        
        return
    
    # Tabs for different modes
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📚 Learn Content",
        "🖼️ Analyze Image",
        "💬 Ask Doubts",
        "📝 Practice Quiz",
        "📊 Progress",
        "🤖 Agent Insights"
    ])
    
    # Tab 1: Learn Content
    with tab1:
        st.header("📚 Learn from Text Content")
        
        input_method = st.radio("Input Method:", ["Text Input", "Upload PDF"], horizontal=True)
        
        if input_method == "Text Input":
            content = st.text_area(
                "Paste your English content here:",
                height=200,
                placeholder="Enter the text you want to learn about..."
            )
        else:
            uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
            content = ""
            if uploaded_file:
                with st.spinner("📄 Extracting text from PDF..."):
                    content = extract_text_from_pdf(uploaded_file)
                    if content:
                        st.success(f"✅ Extracted {len(content)} characters from PDF")
                        with st.expander("📖 View Extracted Text"):
                            st.text_area("PDF Content", content, height=200, disabled=True)
                    else:
                        st.error("Failed to extract text from PDF")
        
        if st.button("🤖 Agent: Analyze & Teach Me", type="primary"):
            if content:
                with st.spinner("🧠 AI Agent is analyzing content and creating learning plan..."):
                    # Show agent thinking process
                    st.markdown("""
                    <div class="agent-thinking">
                        <h4>🤖 Agent Thinking Process:</h4>
                        <p>1. Analyzing content complexity and key concepts...</p>
                        <p>2. Planning optimal learning sequence...</p>
                        <p>3. Generating culturally-contextualized explanations...</p>
                        <p>4. Preparing interactive elements...</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Agent analyzes content
                    analysis = st.session_state.agent.analyze_content(content)
                    st.session_state.analysis = analysis
                    st.session_state.current_content = content
                    
                    # Show analysis
                    st.markdown("### 📊 Agent's Analysis")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if 'main_topic' in analysis:
                            st.info(f"**Topic:** {analysis['main_topic']}")
                            st.info(f"**Difficulty:** {analysis.get('difficulty_level', 'N/A')}")
                    
                    with col2:
                        if 'key_concepts' in analysis:
                            st.info(f"**Key Concepts:** {', '.join(analysis['key_concepts'][:3])}")
                    
                    # Generate translation and explanation
                    explanation = st.session_state.agent.translate_and_explain(content, analysis)
                    
                    st.markdown("### 📖 Your Personalized Lesson")
                    st.markdown(explanation)
                    
                    # Generate summary
                    summary = st.session_state.agent.generate_summary(content)
                    
                    st.markdown("### 📌 Quick Summary")
                    st.markdown(summary)
                    
                    # Track topic learned
                    if 'main_topic' in analysis and analysis['main_topic'] not in st.session_state.topics_learned:
                        st.session_state.topics_learned.append(analysis['main_topic'])
                        # Update agent profile
                        if st.session_state.agent:
                            st.session_state.agent.student_profile['topics_covered'].append(analysis['main_topic'])
                    
                    # Agent proactively suggests next topic
                    if 'main_topic' in analysis:
                        with st.spinner("🤖 Agent is thinking about your next learning step..."):
                            next_topic = st.session_state.agent.suggest_next_topic(analysis['main_topic'])
                            st.info(f"💡 **Agent's Proactive Suggestion:** Consider learning about '{next_topic}' next!")
                    
                    st.markdown("""
                    <div class="success-box">
                        ✅ Learning material prepared! Check the Practice Quiz tab for exercises.
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Please enter some content to learn")
    
    # Tab 2: Analyze Image
    with tab2:
        st.header("🖼️ Multimodal Image Analysis")
        
        uploaded_image = st.file_uploader("Upload an educational image (diagram, chart, screenshot)", type=['png', 'jpg', 'jpeg'])
        additional_context = st.text_input("Additional context or specific question about the image:")
        
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            if st.button("🤖 Agent: Analyze & Explain Image", type="primary"):
                with st.spinner("🔍 Agent is analyzing the image..."):
                    st.markdown("""
                    <div class="agent-thinking">
                        <h4>🤖 Agent Vision Process:</h4>
                        <p>1. Detecting visual elements and text...</p>
                        <p>2. Understanding educational context...</p>
                        <p>3. Generating native language explanation...</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Prepare image for Gemini
                    explanation = st.session_state.agent.analyze_multimodal_input(
                        image_data=image,
                        text=additional_context
                    )
                    
                    st.markdown("### 🎯 Image Explanation")
                    st.markdown(explanation)
    
    # Tab 3: Ask Doubts
    with tab3:
        st.header("💬 Doubt Clarification Chat")
        
        st.markdown("Ask your doubts in any language - the agent will help!")
        
        # Display chat history
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat['question'])
            with st.chat_message("assistant"):
                st.write(chat['answer'])
        
        # Chat input
        user_question = st.chat_input("Ask your doubt here...")
        
        if user_question:
            # Add to chat
            with st.chat_message("user"):
                st.write(user_question)
            
            with st.chat_message("assistant"):
                with st.spinner("🤖 Agent is thinking..."):
                    answer = st.session_state.agent.clarify_doubt(
                        user_question,
                        st.session_state.current_content
                    )
                    st.write(answer)
            
            # Update history
            st.session_state.chat_history.append({
                'question': user_question,
                'answer': answer
            })
            st.rerun()
    
    # Tab 4: Practice Quiz
    with tab4:
        st.header("📝 Adaptive Practice Quiz")
        
        if st.session_state.current_content:
            difficulty = st.select_slider(
                "Difficulty Level",
                options=["easy", "medium", "hard"],
                value="medium"
            )
            
            if st.button("🤖 Agent: Generate Quiz", type="primary"):
                with st.spinner("📝 Agent is creating personalized quiz..."):
                    quiz = st.session_state.agent.generate_interactive_quiz(
                        st.session_state.current_content,
                        difficulty
                    )
                    st.session_state.quiz = quiz
                    st.session_state.quiz_submitted = False  # Reset submission status
            
            if st.session_state.quiz:
                st.markdown("### 🎯 Your Personalized Quiz")
                
                for idx, question in enumerate(st.session_state.quiz):
                    st.markdown(f"#### Question {idx + 1}")
                    st.write(question.get('question', ''))
                    
                    # Only MCQ questions
                    answer = st.radio(
                        "Select your answer:",
                        question.get('options', []),
                        key=f"q_{idx}"
                    )
                    st.session_state.quiz_answers[idx] = answer
                    
                    # Show explanation only after quiz is submitted
                    if st.session_state.quiz_submitted:
                        user_answer = st.session_state.quiz_answers.get(idx, "")
                        correct_answer = question.get('correct', '')
                        is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
                        
                        if is_correct:
                            st.success(f"✅ Correct! {question.get('explanation', '')}")
                        else:
                            st.error(f"❌ Incorrect. Correct answer: {correct_answer}")
                            st.info(f"💡 Explanation: {question.get('explanation', '')}")
                
                if st.button("✅ Submit Quiz"):
                    # Mark quiz as submitted
                    st.session_state.quiz_submitted = True
                    
                    with st.spinner("🤖 Agent is analyzing your performance..."):
                        # Calculate score
                        correct_count = 0
                        total_questions = len(st.session_state.quiz)
                        
                        # Analyze each answer
                        results = []
                        for idx, question in enumerate(st.session_state.quiz):
                            user_answer = st.session_state.quiz_answers.get(idx, "")
                            correct_answer = question.get('correct', '')
                            
                            is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
                            if is_correct:
                                correct_count += 1
                            
                            results.append({
                                'question': question.get('question'),
                                'user_answer': user_answer,
                                'correct_answer': correct_answer,
                                'is_correct': is_correct
                            })
                        
                        # Calculate percentage
                        score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
                        
                        # Agent adaptive learning
                        if score_percentage >= 80:
                            adaptation = {
                                'next_action': 'move_forward',
                                'recommended_difficulty': 'advanced' if difficulty == 'hard' else 'hard',
                                'feedback': 'Excellent! You have mastered this topic.'
                            }
                        elif score_percentage >= 60:
                            adaptation = {
                                'next_action': 'review',
                                'recommended_difficulty': difficulty,
                                'feedback': 'Good progress! Review the concepts and try again.'
                            }
                        else:
                            adaptation = {
                                'next_action': 'deep_dive',
                                'recommended_difficulty': 'easy' if difficulty == 'hard' else difficulty,
                                'feedback': 'Let\'s take it slower. I\'ll explain the concepts in more detail.'
                            }
                    
                    # Display results
                    st.markdown("---")
                    st.markdown("### 📊 Quiz Results")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Score", f"{correct_count}/{total_questions}")
                    with col2:
                        st.metric("Percentage", f"{score_percentage:.0f}%")
                    with col3:
                        if score_percentage >= 80:
                            st.metric("Grade", "A", delta="Excellent")
                        elif score_percentage >= 60:
                            st.metric("Grade", "B", delta="Good")
                        else:
                            st.metric("Grade", "C", delta="Needs Improvement")
                    
                    # Agent's feedback
                    st.markdown(f"""
                    <div class="{'success-box' if score_percentage >= 80 else 'agent-thinking'}">
                        <h4>🤖 Agent's Analysis:</h4>
                        <p><strong>Performance:</strong> {adaptation['feedback']}</p>
                        <p><strong>Next Step:</strong> {adaptation['next_action'].replace('_', ' ').title()}</p>
                        <p><strong>Recommended Level:</strong> {adaptation['recommended_difficulty'].title()}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Detailed breakdown
                    with st.expander("📋 Detailed Answer Review"):
                        for idx, result in enumerate(results):
                            if result['is_correct']:
                                st.success(f"✅ **Q{idx+1}:** Correct!")
                            else:
                                st.error(f"❌ **Q{idx+1}:** Incorrect")
                                st.write(f"Your answer: {result['user_answer']}")
                                st.write(f"Correct answer: {result['correct_answer']}")
                    
                    if score_percentage >= 80:
                        st.balloons()
                    
                    # Track quiz score
                    st.session_state.quiz_scores.append({
                        'score': score_percentage,
                        'correct': correct_count,
                        'total': total_questions,
                        'difficulty': difficulty
                    })
                    
                    # Update student profile
                    st.session_state.agent.student_profile['difficulty_level'] = adaptation['recommended_difficulty']
                    
                    # Force rerun to show explanations
                    st.rerun()
        else:
            st.info("📚 Please learn some content first in the 'Learn Content' tab")
    
    # Tab 5: Progress
    with tab5:
        st.header("📊 Your Learning Progress")
        
        if st.session_state.agent:
            profile = st.session_state.agent.student_profile
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Level", profile['difficulty_level'].title())
            
            with col2:
                st.metric("Topics Covered", len(st.session_state.topics_learned))
            
            with col3:
                st.metric("Doubts Clarified", len(st.session_state.chat_history))
            
            # Quiz performance
            if st.session_state.quiz_scores:
                st.markdown("### 📈 Quiz Performance")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_score = sum(q['score'] for q in st.session_state.quiz_scores) / len(st.session_state.quiz_scores)
                    st.metric("Average Score", f"{avg_score:.1f}%")
                
                with col2:
                    st.metric("Quizzes Taken", len(st.session_state.quiz_scores))
                
                with col3:
                    total_correct = sum(q['correct'] for q in st.session_state.quiz_scores)
                    total_questions = sum(q['total'] for q in st.session_state.quiz_scores)
                    st.metric("Total Correct", f"{total_correct}/{total_questions}")
                
                # Score history
                with st.expander("📊 View Score History"):
                    for idx, quiz_score in enumerate(st.session_state.quiz_scores):
                        st.write(f"**Quiz {idx+1}:** {quiz_score['correct']}/{quiz_score['total']} ({quiz_score['score']:.0f}%) - Difficulty: {quiz_score['difficulty']}")
            
            # Topics learned
            if st.session_state.topics_learned:
                st.markdown("### 📚 Topics You've Learned")
                for topic in st.session_state.topics_learned:
                    st.write(f"✅ {topic}")
            
            st.markdown("### 🎯 Agent's Recommendations")
            st.info("The AI agent continuously adapts to your learning style and pace!")
            
            if st.session_state.current_content:
                with st.spinner("Generating personalized recommendations..."):
                    exercises = st.session_state.agent.generate_practice_exercises(
                        st.session_state.analysis.get('main_topic', 'General') if st.session_state.analysis else 'General',
                        profile['difficulty_level']
                    )
                    
                    st.markdown("### 📚 Recommended Practice Exercises")
                    for exercise in exercises[:5]:
                        if exercise.strip():
                            st.write(exercise)
    
    # Tab 6: Agent Insights
    with tab6:
        st.header("🤖 Agent Insights - Agentic Behavior Dashboard")
        
        st.markdown("""
        <div class="feature-box">
            <h3>🎯 What is Agentic Behavior?</h3>
            <p>This AI agent demonstrates <strong>true autonomy</strong> by making decisions, planning learning paths, 
            and adapting strategies without explicit instructions. Watch how it thinks and acts independently!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.agent:
            # Agent Decision Log
            st.markdown("### 🧠 Agent's Autonomous Decision Log")
            st.caption("Real-time view of the agent's reasoning and decision-making process")
            
            if st.session_state.agent.decision_log:
                for idx, decision in enumerate(reversed(st.session_state.agent.decision_log)):
                    with st.expander(f"Decision #{len(st.session_state.agent.decision_log) - idx}: {decision['type']}", expanded=(idx < 2)):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.markdown(f"**Type:** {decision['type']}")
                            st.markdown(f"**Step:** {decision['timestamp']}")
                        with col2:
                            st.markdown(f"**💭 Agent's Reasoning:**")
                            st.info(decision['reasoning'])
                            st.markdown(f"**⚡ Action Taken:**")
                            st.success(decision['action'])
            else:
                st.info("Start learning to see the agent's decision-making process!")
            
            st.divider()
            
            # Agent's Strategic Recommendation
            st.markdown("### 🎯 Agent's Strategic Recommendation")
            st.caption("Agent autonomously analyzes your progress and suggests next steps")
            
            if st.button("🤔 Ask Agent: What Should I Do Next?", type="primary"):
                with st.spinner("🤖 Agent is analyzing your learning state and deciding..."):
                    # Agent makes autonomous decision
                    context = {
                        "topics_count": len(st.session_state.topics_learned),
                        "quiz_scores": st.session_state.quiz_scores,
                        "quiz_score": st.session_state.quiz_scores[-1]['score'] if st.session_state.quiz_scores else 0
                    }
                    
                    decision = st.session_state.agent.decide_next_action(context)
                    
                    st.markdown(f"""
                    <div class="agent-thinking">
                        <h4>🤖 Agent's Autonomous Decision:</h4>
                        <p><strong>Recommended Action:</strong> {decision['action'].replace('_', ' ').title()}</p>
                        <p><strong>Priority:</strong> {decision['priority'].upper()}</p>
                        <p><strong>Agent's Reasoning:</strong> {decision['reasoning']}</p>
                        <p><strong>Suggestion:</strong> {decision['suggested_content']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.divider()
            
            # Student Profile Analysis
            st.markdown("### 👤 Student Profile (Agent's Understanding)")
            st.caption("How the agent perceives and tracks your learning journey")
            
            profile = st.session_state.agent.student_profile
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Learning Level", profile['difficulty_level'].title())
                st.metric("Learning Style", profile['learning_style'].title())
            
            with col2:
                st.metric("Topics Mastered", len(profile.get('topics_covered', [])))
                st.metric("Active Weak Areas", len(profile.get('weak_areas', [])))
            
            with col3:
                st.metric("Native Language", profile['language'])
                st.metric("Engagement", profile.get('engagement_level', 'high').title())
            
            if profile.get('weak_areas'):
                st.warning(f"🎯 **Agent Identified Weak Areas:** {', '.join(profile['weak_areas'][:3])}")
            
            st.divider()
            
            # Agentic Capabilities
            st.markdown("### ⚡ Agent's Autonomous Capabilities")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **✅ Planning & Strategy:**
                - Analyzes content difficulty autonomously
                - Creates multi-step learning sequences
                - Plans personalized teaching approaches
                
                **✅ Adaptation & Learning:**
                - Adjusts difficulty based on performance
                - Identifies misconceptions automatically
                - Updates teaching strategy in real-time
                """)
            
            with col2:
                st.markdown("""
                **✅ Proactive Behavior:**
                - Suggests next topics without prompting
                - Recommends learning actions strategically
                - Detects when review is needed
                
                **✅ Contextual Understanding:**
                - Maintains student learning history
                - Tracks strengths and weaknesses
                - Adapts to cultural context
                """)
            
            st.divider()
            
            # Comparison
            st.markdown("### 📊 Traditional AI vs Agentic AI")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px;">
                    <h4>🔹 Traditional AI</h4>
                    <ul>
                        <li>Waits for user commands</li>
                        <li>Provides static responses</li>
                        <li>No memory or adaptation</li>
                        <li>One-size-fits-all approach</li>
                        <li>Reactive only</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background-color: #d4edda; padding: 1rem; border-radius: 8px;">
                    <h4>🌟 Our Agentic AI</h4>
                    <ul>
                        <li><strong>Autonomous decision-making</strong></li>
                        <li><strong>Dynamic adaptation</strong></li>
                        <li><strong>Persistent memory & learning</strong></li>
                        <li><strong>Personalized strategies</strong></li>
                        <li><strong>Proactive & Reactive</strong></li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
