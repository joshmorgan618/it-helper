"""
Test suite for ClassifierAgent prompt quality and validation.

This demonstrates how to test your agent prompts for:
- Correct classification
- Edge case handling
- Consistency across runs
- Performance metrics
"""

import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mas_agents.classifier_agent import ClassifierAgent
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class TestClassifierPrompts:
    """Test cases for classifier agent prompt quality"""

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.agent = ClassifierAgent(self.client)
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }

    def run_test(self, test_name: str, ticket_data: dict, expected: dict):
        """
        Run a single test case

        Args:
            test_name: Name of the test
            ticket_data: Input ticket to classify
            expected: Expected classification fields
        """
        print(f"\n{'='*60}")
        print(f"TEST: {test_name}")
        print(f"{'='*60}")
        print(f"Input: {json.dumps(ticket_data, indent=2)}")

        try:
            result = self.agent.process(ticket_data)

            if result is None:
                print(f"❌ FAILED: Agent returned None")
                self.test_results["failed"] += 1
                self.test_results["errors"].append(f"{test_name}: Agent returned None")
                return

            print(f"\nResult: {json.dumps(result, indent=2)}")

            # Validate expected fields
            passed = True
            for key, expected_value in expected.items():
                actual_value = result.get(key)
                if actual_value != expected_value:
                    print(f"❌ MISMATCH on '{key}': expected '{expected_value}', got '{actual_value}'")
                    passed = False
                else:
                    print(f"✓ '{key}': {actual_value}")

            if passed:
                print(f"\n✅ PASSED")
                self.test_results["passed"] += 1
            else:
                print(f"\n❌ FAILED")
                self.test_results["failed"] += 1
                self.test_results["errors"].append(f"{test_name}: Field mismatch")

        except Exception as e:
            print(f"❌ ERROR: {e}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"{test_name}: {str(e)}")

    def test_basic_classifications(self):
        """Test basic, clear-cut classification scenarios"""

        # Test 1: Hardware issue
        self.run_test(
            "Hardware - Printer Issue",
            {
                "subject": "Printer not working",
                "description": "Office printer won't print"
            },
            {
                "category": "hardware",
                "urgency": "medium",
                "expertise_level": "tier1"
            }
        )

        # Test 2: Software issue
        self.run_test(
            "Software - Application Crash",
            {
                "subject": "Excel keeps crashing",
                "description": "Excel crashes every time I open large spreadsheets"
            },
            {
                "category": "software",
                "urgency": "medium",
                "expertise_level": "tier1"
            }
        )

        # Test 3: Network issue - Critical
        self.run_test(
            "Network - Email Outage",
            {
                "subject": "Email server down",
                "description": "Nobody can send or receive emails company-wide"
            },
            {
                "category": "network",
                "urgency": "critical",
                "expertise_level": "tier2"
            }
        )

        # Test 4: Access issue
        self.run_test(
            "Access - Password Reset",
            {
                "subject": "Can't login",
                "description": "Forgot my password and can't access my account"
            },
            {
                "category": "access",
                "urgency": "medium",
                "expertise_level": "tier1"
            }
        )

    def test_urgency_keywords(self):
        """Test that urgency keywords are properly detected"""

        # High urgency with deadline
        self.run_test(
            "Urgency - Deadline Driven",
            {
                "subject": "URGENT: Can't access payroll",
                "description": "Need to submit timesheets by EOD today"
            },
            {
                "category": "access",
                "urgency": "high"
            }
        )

        # Low urgency - Feature request
        self.run_test(
            "Urgency - Feature Request",
            {
                "subject": "Feature Request: Dark Mode",
                "description": "Would be nice to have dark mode in the app"
            },
            {
                "category": "software",
                "urgency": "low"
            }
        )

    def test_edge_cases(self):
        """Test edge cases and ambiguous scenarios"""

        # Vague description
        self.run_test(
            "Edge Case - Vague Description",
            {
                "subject": "Computer problems",
                "description": "My computer is slow"
            },
            {
                # Should still provide a classification
                # Exact values may vary, but should not fail
            }
        )

        # Multiple issues mentioned
        self.run_test(
            "Edge Case - Multiple Issues",
            {
                "subject": "Can't print and internet is slow",
                "description": "The printer won't work and the WiFi is really slow today"
            },
            {
                # Should pick primary issue
                # Either hardware (printer) or network (WiFi) is acceptable
            }
        )

    def test_consistency(self):
        """Test that same input produces consistent results"""
        print(f"\n{'='*60}")
        print(f"TEST: Consistency Check")
        print(f"{'='*60}")

        ticket = {
            "subject": "Laptop won't start",
            "description": "My laptop won't turn on at all"
        }

        results = []
        for i in range(3):
            result = self.agent.process(ticket)
            if result:
                results.append(result)
                print(f"Run {i+1}: category={result['category']}, urgency={result['urgency']}")

        if len(results) == 3:
            # Check if all results are the same
            if all(r['category'] == results[0]['category'] for r in results) and \
               all(r['urgency'] == results[0]['urgency'] for r in results) and \
               all(r['expertise_level'] == results[0]['expertise_level'] for r in results):
                print("✅ PASSED: Consistent classifications")
                self.test_results["passed"] += 1
            else:
                print("❌ FAILED: Inconsistent classifications")
                self.test_results["failed"] += 1
        else:
            print("❌ FAILED: Some runs returned None")
            self.test_results["failed"] += 1

    def print_summary(self):
        """Print test summary and metrics"""
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Passed: {self.test_results['passed']}")
        print(f"Failed: {self.test_results['failed']}")
        print(f"Total: {self.test_results['passed'] + self.test_results['failed']}")

        if self.test_results["errors"]:
            print(f"\nErrors:")
            for error in self.test_results["errors"]:
                print(f"  - {error}")

        print(f"\n{'='*60}")
        print(f"AGENT METRICS")
        print(f"{'='*60}")
        metrics = self.agent.get_metrics()
        print(json.dumps(metrics, indent=2))

        # Success rate
        total = metrics.get("total_requests", 0)
        if total > 0:
            success_rate = (metrics.get("successful_parses", 0) / total) * 100
            print(f"\nOverall Success Rate: {success_rate:.1f}%")
            print(f"Average Response Time: {metrics.get('average_response_time', 0):.2f}s")


def main():
    """Run all tests"""
    print("Starting ClassifierAgent Prompt Quality Tests")
    print("=" * 60)

    tester = TestClassifierPrompts()

    # Run test suites
    tester.test_basic_classifications()
    tester.test_urgency_keywords()
    tester.test_edge_cases()
    tester.test_consistency()

    # Print summary
    tester.print_summary()


if __name__ == "__main__":
    main()
