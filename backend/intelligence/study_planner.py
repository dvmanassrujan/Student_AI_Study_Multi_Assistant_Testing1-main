"""
Model-Free Intelligent Study Planner Engine.
Calculates personalized daily and weekly academic study timetables using:
- Subject Priority (High, Medium, Low)
- Available Daily Study Hours (1-12h)
- Target Timeline / Exam Dates
- Topic Difficulty Calibration (Beginner, Intermediate, Advanced)
- Spaced Repetition Revision Intervals (Ebbinghaus Forgetting Curve)
- Daily Pomodoro Study Targets & Time-Blocking
- Milestone Checkpoints & Progress Tracking
"""

import re
import math
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional, Tuple

# =========================================================================
# 1. Curated Curriculum Taxonomies for Subtopic Breakdown
# =========================================================================

CURRICULUM_TAXONOMIES: Dict[str, List[str]] = {
    "python": [
        "Syntax, Variables, Dynamic Typing & Control Structures",
        "Functions, Scope, Arguments (*args, **kwargs) & Recursion",
        "Data Structures: Lists, Dictionaries, Sets & Tuples",
        "Object-Oriented Programming (Classes, Inheritance, Dunder Methods)",
        "Error Handling, Exceptions & Context Managers (with statement)",
        "Iterators, Generators (yield) & List Comprehensions",
        "Standard Library Power Tools: collections, itertools, functools",
        "File I/O, Serialization (JSON, Pickle) & Regex",
        "Decorators, Closures & Functional Programming Patterns",
        "Unit Testing (unittest, pytest) & Code Optimization"
    ],
    "machine learning": [
        "Linear Algebra & Multivariable Calculus Foundations",
        "Probability Distributions, Statistics & Hypothesis Testing",
        "Data Preprocessing, Cleaning & Feature Engineering",
        "Supervised Learning: Linear & Logistic Regression",
        "Decision Trees, Random Forests & Ensemble Methods",
        "Support Vector Machines & Kernel Methods",
        "Unsupervised Learning: K-Means Clustering & PCA",
        "Gradient Descent Optimizers & Regularization (L1, L2)",
        "Neural Networks Architecture & Backpropagation",
        "Model Evaluation: Cross-Validation, ROC-AUC & F1 Score"
    ],
    "data structures": [
        "Time & Space Complexity Analysis (Big-O, Omega, Theta)",
        "Arrays, Dynamic Arrays & String Manipulation",
        "Two Pointers & Sliding Window Algorithmic Techniques",
        "Singly & Doubly Linked Lists (Fast & Slow Pointers)",
        "Stacks, Queues & Monotonic Stack Applications",
        "Hash Tables, Collision Resolution & Hash Maps",
        "Binary Trees, Traversals (Pre, In, Post, Level-Order)",
        "Binary Search Trees (BST), AVL & Red-Black Trees",
        "Heaps, Priority Queues & Heap Sort",
        "Graphs: Adjacency Lists, BFS, DFS & Topological Sort"
    ],
    "algorithms": [
        "Divide and Conquer: Merge Sort & Quick Sort Analysis",
        "Binary Search & Ternary Search Variations",
        "Greedy Algorithms: Activity Selection & Huffman Coding",
        "Dynamic Programming: 1D Memoization & Tabulation",
        "Dynamic Programming: 2D Grids, Knapsack & Subsequences",
        "Graph Algorithms: Dijkstra, Bellman-Ford & Shortest Paths",
        "Minimum Spanning Trees: Kruskal & Prim Algorithms",
        "Backtracking: N-Queens, Sudoku & Subset Generation",
        "Bit Manipulation & Bitmasking Techniques",
        "String Algorithms: KMP, Rabin-Karp & Trie Traversal"
    ],
    "calculus": [
        "Functions, Limits & Continuity Fundamentals",
        "Definition of Derivative & Instantaneous Rate of Change",
        "Power Rule, Product Rule, Quotient Rule & Chain Rule",
        "Implicit Differentiation & Related Rates Problems",
        "Applications of Derivatives: Extrema & Curve Sketching",
        "Mean Value Theorem & L'Hopital Rule",
        "Antiderivatives, Indefinite Integrals & Riemann Sums",
        "Fundamental Theorem of Calculus & Definite Integrals",
        "Integration Techniques: Substitution & By Parts",
        "Applications of Integration: Area & Volume of Revolution"
    ],
    "biology": [
        "Cell Structure: Prokaryotes vs Eukaryotes & Organelles",
        "Biomolecules: Carbohydrates, Lipids, Proteins & Nucleic Acids",
        "Cell Membrane Transport, Osmosis & Active Transport",
        "Cellular Respiration: Glycolysis, Krebs Cycle & ATP",
        "Photosynthesis: Light Reactions & Calvin Cycle",
        "Cell Division: Mitosis, Meiosis & Cell Cycle Checkpoints",
        "Mendelian Genetics, Punnett Squares & Pedigree Analysis",
        "Molecular Genetics: DNA Replication, Transcription & Translation",
        "Evolutionary Biology, Natural Selection & Phylogeny",
        "Ecosystem Dynamics, Nutrient Cycles & Population Ecology"
    ]
}


def _resolve_duration_days(duration: str, exam_date: Optional[str] = None) -> int:
    """Calculates number of study days from duration string or exam date."""
    if exam_date:
        try:
            target = datetime.strptime(exam_date.strip(), "%Y-%m-%d").date()
            diff = (target - date.today()).days
            if diff > 0:
                return min(365, diff)
        except Exception:
            pass

    clean_dur = (duration or "1 Week").lower().strip()
    if "1 day" in clean_dur:
        return 1
    elif "3 day" in clean_dur:
        return 3
    elif "1 week" in clean_dur:
        return 7
    elif "2 week" in clean_dur:
        return 14
    elif "1 month" in clean_dur or "4 week" in clean_dur:
        return 30
    elif "2 month" in clean_dur:
        return 60
    elif "3 month" in clean_dur or "semester" in clean_dur:
        return 90

    # Extract any digits: e.g. "5 days"
    digits = re.findall(r"\d+", clean_dur)
    if digits:
        val = int(digits[0])
        if "week" in clean_dur:
            return min(365, val * 7)
        if "month" in clean_dur:
            return min(365, val * 30)
        return max(1, min(365, val))

    return 7


def _get_subtopics_for_topic(topic: str, target_count: int) -> List[str]:
    """Retrieves or algorithmically generates modular subtopics."""
    clean_topic = topic.lower().strip()
    matched = None

    for k, sub_list in CURRICULUM_TAXONOMIES.items():
        if k in clean_topic or clean_topic in k:
            matched = sub_list
            break

    if matched:
        # Sample or cycle up to target_count
        result = []
        for i in range(target_count):
            result.append(matched[i % len(matched)])
        return result

    # Algorithmic curriculum decomposition for arbitrary subject
    title = topic.title()
    templates = [
        f"{title} Foundations & Core Terminology",
        f"Core Principles & Theoretical Mechanics of {title}",
        f"Key Methodologies & Standard Problem-Solving in {title}",
        f"Intermediate Applied Concepts & Frameworks in {title}",
        f"Deep Dive: Complex Components & Case Studies in {title}",
        f"Practical Exercises, Edge Cases & Synthesis in {title}",
        f"Advanced Applications & Performance Optimization in {title}",
        f"Cross-Disciplinary Connections & Real-World Projects in {title}",
        f"Comprehensive Review, Mock Diagnostic & Self-Assessment"
    ]
    return [templates[i % len(templates)] for i in range(target_count)]


# =========================================================================
# 2. Study Plan Generator Engine
# =========================================================================

def generate_study_plan_schedule(
    topic: str,
    level: str = "Beginner",
    duration: str = "1 Week",
    hours_per_day: float = 2.0,
    goals: str = "",
    priority: str = "Medium",
    exam_date: Optional[str] = None,
    completion_percentage: float = 0.0
) -> str:
    """
    Generates a personalized, mathematically grounded daily and weekly study plan.
    Incorporates Ebbinghaus revision intervals, Pomodoro time blocks,
    difficulty multipliers, and progress tracking checklists.
    """
    clean_topic = (topic or "Python Programming").strip()
    safe_level = level if level in ["Beginner", "Intermediate", "Advanced"] else "Beginner"
    safe_priority = priority if priority in ["High", "Medium", "Low"] else "Medium"
    try:
        safe_hours = max(1.0, min(14.0, float(hours_per_day or 2.0)))
    except (TypeError, ValueError):
        safe_hours = 2.0

    total_days = _resolve_duration_days(duration, exam_date)
    total_hours = round(total_days * safe_hours, 1)

    # Difficulty & Priority Weights
    diff_multipliers = {"Beginner": 1.0, "Intermediate": 1.3, "Advanced": 1.6}
    diff_mult = diff_multipliers.get(safe_level, 1.0)

    # Subtopic curriculum list
    subtopics = _get_subtopics_for_topic(clean_topic, total_days)

    # Calculate Pomodoro sessions per day (25m study + 5m break = 30m block)
    pomodoro_blocks_per_day = max(2, int(safe_hours * 2))

    # Determine spaced repetition revision days based on Ebbinghaus curve
    revision_days = set()
    for d_idx in range(1, total_days + 1):
        if d_idx in [2, 4, 7, 14, 21, 28, 45, 60]:
            revision_days.add(d_idx)
    # The last day is always a mock exam & comprehensive review
    revision_days.add(total_days)

    lines = [
        f"# 📅 Intelligent Academic Study Plan: {clean_topic.title()}",
        f"**Target Duration:** `{total_days} Days` ({duration}) | **Daily Commitment:** `{safe_hours:.1f} Hours/Day` | **Total Budget:** `{total_hours} Hours`",
        f"**Knowledge Level:** `{safe_level}` (Difficulty Factor: `{diff_mult}x`) | **Subject Priority:** `{safe_priority}`",
        f"**Current Progress:** `{completion_percentage:.1f}% Complete`",
        f"**Strategic Goals:** {goals if goals.strip() else 'Build mastery of core principles, practice active recall, and achieve exam readiness.'}\n",
        "---",
        "## 🧭 Executive Pacing & Methodology\n",
        f"- ⏱️ **Daily Structure:** Each day consists of **{pomodoro_blocks_per_day} Pomodoro blocks** (25 min intense study + 5 min rest).",
        f"- 🧠 **Active Recall:** Spend the first 15 minutes of every session testing yourself without notes on yesterday's material.",
        f"- 🔄 **Spaced Repetition:** Scheduled revision checkpoints on days: `{', '.join(f'Day {d}' for d in sorted(revision_days))}`.",
        f"- 🎯 **Milestone Target:** Complete `{round(100.0 / max(1, total_days), 1)}%` of the curriculum daily to stay on track.\n",
        "---",
        "## 🗓️ Day-by-Day Milestone Timetable\n"
    ]

    for day_num in range(1, total_days + 1):
        topic_idx = day_num - 1
        day_topic = subtopics[topic_idx]
        is_revision = day_num in revision_days

        p1_time = round(safe_hours * 0.4, 1)
        p2_time = round(safe_hours * 0.4, 1)
        p3_time = round(safe_hours * 0.2, 1)

        rev_badge = " 🔄 *(Spaced Revision Checkpoint)*" if is_revision else ""
        lines.append(f"### 📍 Day {day_num} of {total_days}: {day_topic}{rev_badge}")
        lines.append(f"**Total Allocation:** `{safe_hours}h` ({pomodoro_blocks_per_day} Pomodoros)\n")

        lines.append(f"- [ ] **Block 1 (Deep Theory & Concepts - {p1_time}h):**")
        lines.append(f"  - Study core definitions and conceptual mechanics of *{day_topic}*.")
        lines.append(f"  - Annotate key equations, syntax structures, and relationships.")

        lines.append(f"- [ ] **Block 2 (Active Practice & Implementation - {p2_time}h):**")
        lines.append(f"  - Complete 3-5 hands-on exercises or write runnable code implementing these principles.")
        lines.append(f"  - Formulate 2 self-quiz flashcards on subtle edge cases.")

        if is_revision:
            lines.append(f"- [ ] **Block 3 (Spaced Repetition & Self-Testing - {p3_time}h):**")
            lines.append(f"  - Rapid 15-minute flashcard recall test covering Days 1 through {day_num - 1}.")
            lines.append(f"  - Review weak topics and update personal knowledge gap log.")
        else:
            lines.append(f"- [ ] **Block 3 (Daily Synthesis & Wrap-Up - {p3_time}h):**")
            lines.append(f"  - Write a 3-sentence summary of today's core learning from memory.")
            lines.append(f"  - Verify understanding and check off daily study target.")

        lines.append("")

    # Weekly Overview & Review Schedule
    lines.extend([
        "---",
        "## 📊 Weekly Milestones & Assessment Plan\n"
    ])

    num_weeks = max(1, math.ceil(total_days / 7))
    for w in range(1, num_weeks + 1):
        w_start = (w - 1) * 7 + 1
        w_end = min(total_days, w * 7)
        lines.append(f"#### 🏆 Week {w} Milestone (Days {w_start} - {w_end}):")
        lines.append(f"- [ ] Complete all assigned modules and exercises for Days {w_start} to {w_end}.")
        lines.append(f"- [ ] Take a timed 10-question mock assessment on Friday/Saturday.")
        lines.append(f"- [ ] Conduct a 45-minute synthesis review to consolidate weak spots.\n")

    lines.extend([
        "---",
        "## 📈 Student Progress Tracker",
        "To update your study progress, check off completed days above and log your percentage in the AI Assistant.",
        "",
        "*Study plan generated deterministically using active recall scheduling and cognitive load optimization.*"
    ])

    return "\n".join(lines)


# =========================================================================
# 3. Interactive Progress Updater
# =========================================================================

def calculate_completion_status(
    completed_days: int,
    total_days: int
) -> Dict[str, Any]:
    """Calculates updated progress percentage, remaining hours, and pace assessment."""
    safe_total = max(1, total_days)
    safe_done = max(0, min(safe_total, completed_days))
    pct = round((safe_done / safe_total) * 100.0, 1)

    if pct >= 100.0:
        status = "Complete 🎉"
        feedback = "Outstanding! You have completed the entire study curriculum. Ready for your final exam!"
    elif pct >= 60.0:
        status = "On Track 🚀"
        feedback = "Great progress! You are past the halfway mark. Maintain your daily revision habit."
    elif pct >= 25.0:
        status = "Steady Momentum 📈"
        feedback = "Solid foundation established. Focus on active recall exercises to lock in retention."
    else:
        status = "Early Phase 🌱"
        feedback = "Beginning phase. Complete your first 3 consecutive days to build a strong study streak."

    return {
        "completed_days": safe_done,
        "total_days": safe_total,
        "completion_percentage": pct,
        "status": status,
        "feedback": feedback
    }

