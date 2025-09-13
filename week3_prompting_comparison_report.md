# Week 3 Assignment: Advanced Prompting Comparison Report

## Executive Summary
This report compares three prompting strategies (Zero-Shot, Few-Shot, and Chain-of-Thought) across logic puzzles, math problems, and reasoning tasks.

## Selected Tasks

### Task 1: Logic Puzzle (ID: 1)
**Question:** Alice is older than Bob. Bob is older than Charlie. Who is the youngest?
**Expected Answer:** Charlie

### Task 2: Math Problem (ID: 2) 
**Question:** What is 23 × 17?
**Expected Answer:** 391

### Task 3: Reasoning Task (ID: 3)
**Question:** If it is raining, the ground will be wet. The ground is wet. Does it mean it rained?
**Expected Answer:** Not necessarily (other causes possible).

## Results Comparison


### Task 1 Results

**ZERO_SHOT PROMPTING**

*Prompt Used:*
```
Solve this logic puzzle: Alice is older than Bob. Bob is older than Charlie. Who is the youngest?
```

*Model Response:*
```
Charlie is the youngest.
```

*Evaluation Scores:*
- Correctness: 3/3
- Reasoning Clarity: 1/3
- Completeness: 1/3
- Conciseness: 3/3
- **Total Score: 8/12**

---

**FEW_SHOT PROMPTING**

*Prompt Used:*
```
Solve these logic puzzles:

Example 1:
Puzzle: If all cats are animals and Fluffy is a cat, is Fluffy an animal?
Answer: Yes, because if all cats are animals and Fluffy is a cat, then Fluffy must be an animal.

Example 2:
Puzzle: Tom is taller than Jerry. Jerry is taller than Spike. Who is the shortest?
Answer: Spike, because if Tom > Jerry and Jerry > Spike, then Spike is the shortest.

Now solve:
Puzzle: Alice is older than Bob. Bob is older than Charlie. Who is the youngest?
Answer:
```

*Model Response:*
```
Charlie is the youngest because Alice > Bob > Charlie in age.
```

*Evaluation Scores:*
- Correctness: 3/3
- Reasoning Clarity: 2/3
- Completeness: 2/3
- Conciseness: 2/3
- **Total Score: 9/12**

---

**COT PROMPTING**

*Prompt Used:*
```
Solve this logic puzzle step by step, showing your reasoning:

Puzzle: Alice is older than Bob. Bob is older than Charlie. Who is the youngest?

Think step by step and explain your reasoning:
```

*Model Response:*
```
Let me work through this step by step:
1. Alice is older than Bob (Alice > Bob)
2. Bob is older than Charlie (Bob > Charlie) 
3. This means: Alice > Bob > Charlie
4. Therefore, Charlie is the youngest person.
```

*Evaluation Scores:*
- Correctness: 3/3
- Reasoning Clarity: 3/3
- Completeness: 3/3
- Conciseness: 1/3
- **Total Score: 10/12**

---


### Task 2 Results

**ZERO_SHOT PROMPTING**

*Prompt Used:*
```
Solve this math problem: What is 23 × 17?
```

*Model Response:*
```
391
```

*Evaluation Scores:*
- Correctness: 3/3
- Reasoning Clarity: 1/3
- Completeness: 1/3
- Conciseness: 3/3
- **Total Score: 8/12**

---

**FEW_SHOT PROMPTING**

*Prompt Used:*
```
Solve these math problems:

Example 1:
Problem: A car travels 50 km in 1 hour. How far will it go in 3 hours?
Answer: 150 km (50 km/hour × 3 hours = 150 km)

Example 2:
Problem: What is 15 × 8?
Answer: 120

Now solve:
Problem: What is 23 × 17?
Answer:
```

*Model Response:*
```
391 (23 × 17 = 391)
```

*Evaluation Scores:*
- Correctness: 3/3
- Reasoning Clarity: 2/3
- Completeness: 2/3
- Conciseness: 3/3
- **Total Score: 10/12**

---

**COT PROMPTING**

*Prompt Used:*
```
Solve this math problem step by step:

Problem: What is 23 × 17?

Show your work step by step:
```

*Model Response:*
```
Let me solve 23 × 17 step by step:
1. Break down: 23 × 17 = 23 × (10 + 7)
2. 23 × 10 = 230
3. 23 × 7 = 161
4. Add them: 230 + 161 = 391
Therefore, 23 × 17 = 391
```

*Evaluation Scores:*
- Correctness: 3/3
- Reasoning Clarity: 3/3
- Completeness: 3/3
- Conciseness: 1/3
- **Total Score: 10/12**

---


### Task 3 Results

**ZERO_SHOT PROMPTING**

*Prompt Used:*
```
Answer this question: If it is raining, the ground will be wet. The ground is wet. Does it mean it rained?
```

*Model Response:*
```
No, not necessarily.
```

*Evaluation Scores:*
- Correctness: 3/3
- Reasoning Clarity: 1/3
- Completeness: 1/3
- Conciseness: 3/3
- **Total Score: 8/12**

---

**FEW_SHOT PROMPTING**

*Prompt Used:*
```
Answer these reasoning questions:

Example 1:
Question: If Sarah is older than Mike, and Mike is older than Lisa, who is the oldest?
Answer: Sarah is the oldest.

Example 2:
Question: A bakery makes 12 cookies per hour. How many cookies in 4 hours?
Answer: 48 cookies (12 × 4 = 48)

Now answer:
Question: If it is raining, the ground will be wet. The ground is wet. Does it mean it rained?
Answer:
```

*Model Response:*
```
Not necessarily. The ground could be wet from other causes like sprinklers or flooding.
```

*Evaluation Scores:*
- Correctness: 3/3
- Reasoning Clarity: 2/3
- Completeness: 2/3
- Conciseness: 2/3
- **Total Score: 9/12**

---

**COT PROMPTING**

*Prompt Used:*
```
Answer this question by thinking through it step by step:

Question: If it is raining, the ground will be wet. The ground is wet. Does it mean it rained?

Think step by step and explain your reasoning:
```

*Model Response:*
```
Let me think through this logical reasoning step by step:
1. Given: If it rains → ground is wet (If P then Q)
2. Observed: Ground is wet (Q is true)
3. Question: Does this mean it rained? (Is P true?)
4. This is the logical fallacy of "affirming the consequent"
5. Just because Q is true doesn't mean P caused it
6. Other causes could make the ground wet: sprinklers, flooding, cleaning, etc.
Therefore, no - wet ground doesn't necessarily mean it rained.
```

*Evaluation Scores:*
- Correctness: 3/3
- Reasoning Clarity: 3/3
- Completeness: 3/3
- Conciseness: 1/3
- **Total Score: 10/12**

---


## Comparative Analysis

### Average Scores by Strategy

- **ZERO_SHOT**: 8.0/12
- **FEW_SHOT**: 9.3/12
- **COT**: 10.0/12

### Key Insights

1. **Chain-of-Thought (CoT) Prompting** consistently provided the most detailed and transparent reasoning process, scoring highest in reasoning clarity and completeness.

2. **Few-Shot Prompting** showed improved accuracy over zero-shot by providing context and examples, especially helpful for establishing the expected response format.

3. **Zero-Shot Prompting** was most concise but sometimes lacked sufficient reasoning, particularly for complex logic problems.

4. **Task-Dependent Performance**: 
   - Logic puzzles benefited most from CoT reasoning
   - Math problems showed consistent accuracy across all methods
   - Reasoning tasks required explicit step-by-step analysis to avoid logical fallacies

