# Agent Prompt Engineering Improvements

This document explains the improvements made to `classifier_agent.py` that you can use as a template for your other agents.

## What Changed

### 1. **Enhanced System Prompt** (Lines 24-127)

The prompt now includes:

#### **Clear Role Definition**
```
You are a Classifier Agent for IT support with expertise in triaging technical issues.
```
- Establishes expertise and authority
- Sets clear expectations

#### **Detailed Guidelines** (Lines 38-55)
- Explicit definitions for each category, urgency level, and expertise tier
- Examples of what falls into each classification
- Removes ambiguity

#### **Reasoning Process (Chain of Thought)** (Lines 57-62)
```
Before classifying, think through:
1. What is the primary technical component mentioned?
2. How many users are affected and is work blocked?
3. Does this require specialized knowledge?
4. Are there any urgency keywords?
```
- Guides the model to "think" before answering
- Improves accuracy by breaking down the decision process

#### **Few-Shot Examples** (Lines 64-104)
- 5 diverse examples showing input → analysis → output
- Demonstrates the reasoning process
- Covers different categories, urgency levels, and complexity

#### **Edge Case Handling** (Lines 106-110)
- Explicit instructions for vague/missing data
- How to handle multiple categories
- Default values when unclear

#### **Validation Requirements** (Lines 112-118)
- Self-check before returning
- Reduces malformed responses

### 2. **Response Validation** (Lines 129-161)

```python
def _validate_classification(self, classification: Dict[str, Any]) -> tuple[bool, Optional[str]]:
```

**What it does:**
- Checks all required fields are present
- Validates values against allowed lists
- Ensures reasoning is meaningful (>10 characters)
- Returns clear error messages

**Why it matters:**
- Catches bad outputs before they cause downstream errors
- Provides actionable feedback for debugging
- Improves reliability

### 3. **Metrics Tracking** (Lines 15-22, 163-195)

```python
self.metrics = {
    "total_requests": 0,
    "successful_parses": 0,
    "failed_parses": 0,
    "validation_failures": 0,
    "average_response_time": 0.0
}
```

**What it tracks:**
- JSON parse success rate
- Validation success rate
- Average response time
- Total requests processed

**How to use it:**
```python
# After processing tickets
metrics = classifier_agent.get_metrics()
print(f"Success rate: {metrics['parse_success_rate']:.1%}")
print(f"Avg response time: {metrics['average_response_time']:.2f}s")
```

**Why it matters:**
- Identify when prompts degrade
- A/B test different prompt versions
- Monitor production performance

### 4. **Temperature Control** (Line 221)

```python
response = self.call_claude(
    messages=messages,
    system_prompt=system_prompt,
    temperature=0.3  # Lower = more consistent
)
```

**Temperature guide:**
- **0.0-0.3**: Deterministic, factual tasks (classification, data extraction)
- **0.5-0.7**: Balanced creativity and consistency
- **0.8-1.0**: Creative tasks (writing, brainstorming)

For ClassifierAgent: 0.3 ensures consistent classifications

### 5. **Enhanced Logging** (Lines 252-257)

```python
self.log_action(
    f"Classified as: {classification.get('category')} - "
    f"{classification.get('urgency')} - "
    f"{classification.get('expertise_level')} "
    f"(took {response_time:.2f}s)"
)
```

Now includes timing information for performance monitoring.

### 6. **Type Hints** (Throughout)

```python
def process(self, parsed_ticket: Dict[str, Any]) -> Optional[Dict[str, Any]]:
```

- Better IDE support
- Clearer expectations
- Easier debugging

## How to Apply to Other Agents

### Template Structure

```python
from .base_agent import BaseAgent
import json
import time
from typing import Optional, Dict, Any

class YourAgent(BaseAgent):
    def __init__(self, client):
        super().__init__(client, name="YourAgent")
        # Add metrics tracking
        self.metrics = {
            "total_requests": 0,
            "successful_parses": 0,
            "failed_parses": 0,
            "validation_failures": 0,
            "average_response_time": 0.0
        }

    def _build_enhanced_prompt(self) -> str:
        """Build prompt with guidelines, examples, edge cases"""
        return """
        [Role Definition]

        GUIDELINES:
        [Clear definitions]

        REASONING PROCESS:
        [Chain of thought steps]

        FEW-SHOT EXAMPLES:
        [3-5 examples with input/analysis/output]

        EDGE CASE HANDLING:
        [How to handle ambiguity]

        VALIDATION REQUIREMENTS:
        [Self-check before returning]

        [Expected output format]
        """

    def _validate_response(self, response: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate the response structure and values"""
        # Check required fields
        # Validate field values
        # Return (is_valid, error_message)
        pass

    def _update_metrics(self, response_time: float, parse_success: bool, validation_success: bool):
        """Update internal metrics"""
        self.metrics["total_requests"] += 1
        if parse_success:
            self.metrics["successful_parses"] += 1
        else:
            self.metrics["failed_parses"] += 1
        if not validation_success:
            self.metrics["validation_failures"] += 1
        # Update rolling average
        total = self.metrics["total_requests"]
        current_avg = self.metrics["average_response_time"]
        self.metrics["average_response_time"] = ((current_avg * (total - 1)) + response_time) / total

    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        total = self.metrics["total_requests"]
        if total == 0:
            return self.metrics
        return {
            **self.metrics,
            "parse_success_rate": self.metrics["successful_parses"] / total,
            "validation_success_rate": 1 - (self.metrics["validation_failures"] / total)
        }

    def process(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Main processing method with full error handling"""
        self.log_action("Processing...")
        start_time = time.time()

        # Build prompt
        system_prompt = self._build_enhanced_prompt()
        messages = [{"role": "user", "content": f"Input: {json.dumps(input_data)}"}]

        # Call Claude with appropriate temperature
        response = self.call_claude(messages, system_prompt, temperature=0.3)
        response_time = time.time() - start_time

        if not response:
            self._update_metrics(response_time, False, False)
            return None

        # Parse JSON
        try:
            parsed = json.loads(response)
        except json.JSONDecodeError as e:
            self.log_action(f"Parse failed: {e}")
            self._update_metrics(response_time, False, False)
            return None

        # Validate
        is_valid, error = self._validate_response(parsed)
        if not is_valid:
            self.log_action(f"Validation failed: {error}")
            self._update_metrics(response_time, True, False)
            return None

        # Success
        self._update_metrics(response_time, True, True)
        return parsed
```

## Agent-Specific Customizations

### IntakeAgent
- **Temperature**: 0.4 (slight creativity for improving descriptions)
- **Examples**: Show subject line improvements (vague → clear)
- **Validation**: Check email format, subject not empty
- **Edge cases**: Missing email, very short descriptions

### DiagnosticAgent
- **Temperature**: 0.5 (balance between consistency and diagnostic creativity)
- **Examples**: Different issue types with their diagnoses
- **Validation**: At least 2 potential causes, 2 recommended tests
- **Edge cases**: Insufficient information, multiple symptoms

### SolutionAgent
- **Temperature**: 0.6 (needs creativity for solutions)
- **Examples**: Show how to use past solutions, structure steps
- **Validation**: Solution has steps, confidence is justified
- **Edge cases**: No past solutions available, conflicting past solutions

### FetchAgent
- Note: This agent doesn't use Claude, so improvements would focus on:
  - Better error handling
  - Metrics on search quality
  - Logging of search effectiveness

## Testing Your Improved Prompts

See `tests/test_classifier_agent_prompts.py` for a complete testing framework.

### Key Test Categories

1. **Basic Functionality**
   - Known inputs → expected outputs
   - All categories/types covered

2. **Edge Cases**
   - Vague descriptions
   - Missing data
   - Ambiguous scenarios

3. **Consistency**
   - Same input → same output (with low temperature)
   - Run same test 3-5 times

4. **Performance**
   - Response time acceptable
   - Success rate > 95%
   - No validation failures

### Running Tests

```bash
python tests/test_classifier_agent_prompts.py
```

## Monitoring in Production

### Log Metrics Periodically

```python
# In your workflow or main app
if ticket_count % 100 == 0:  # Every 100 tickets
    metrics = classifier_agent.get_metrics()
    print(f"Classifier metrics: {metrics}")
    # Could also log to file or monitoring service
```

### Watch for Degradation

- Success rate dropping below 90%? Investigate prompts
- Response time increasing? Model may be struggling
- Validation failures? Prompt may need more examples

### A/B Testing New Prompts

```python
# Keep two versions
classifier_v1 = ClassifierAgent(client)  # Current prompt
classifier_v2 = ClassifierAgent(client)  # New prompt

# Randomly assign
import random
agent = classifier_v1 if random.random() < 0.5 else classifier_v2

# Compare metrics after N tickets
```

## Quick Reference: When to Use Each Temperature

| Agent | Task Type | Temperature | Reasoning |
|-------|-----------|-------------|-----------|
| IntakeAgent | Data extraction + slight improvement | 0.4 | Need consistency but allow minor creativity for improving descriptions |
| ClassifierAgent | Strict categorization | 0.3 | Need very consistent classifications |
| DiagnosticAgent | Analysis with creativity | 0.5 | Balance between consistent reasoning and creative problem-solving |
| SolutionAgent | Creative problem-solving | 0.6 | Need creativity for solutions but not random |

## Next Steps

1. **Apply template to IntakeAgent**
   - Add few-shot examples of subject/description improvements
   - Add email validation
   - Add metrics tracking

2. **Apply template to DiagnosticAgent**
   - Add examples of different issue types
   - Add validation for causes/tests
   - Add temperature control

3. **Apply template to SolutionAgent**
   - Add examples showing past solution usage
   - Add confidence justification
   - Add step structure validation

4. **Create test suite for each agent**
   - Use `test_classifier_agent_prompts.py` as template
   - Build test cases specific to each agent's function

5. **Set up production monitoring**
   - Log metrics every N requests
   - Alert on success rate < 90%
   - Dashboard for tracking over time
