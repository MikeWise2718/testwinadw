#!/usr/bin/env python3
"""Test the format_issue_message function in a workflow context."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from adw_modules.workflow_ops import format_issue_message

# Test various messages that would appear in workflow phases
test_messages = [
    # Planning phase messages
    ("✅ Starting planning phase", "ops"),
    ("✅ Issue classified as: /feature", "ops"),
    ("✅ Working on branch: feature-123", "ops"),
    ("✅ Implementation plan created", "sdlc_planner"),

    # Build phase messages
    ("✅ Starting build phase", "ops"),
    ("✅ Build completed successfully", "sdlc_implementor"),
    ("❌ Build failed with errors", "sdlc_implementor"),

    # Test phase messages
    ("✅ Starting test suite", "ops"),
    ("✅ Running application tests...", "test_agent"),
    ("📊 Final test results:\n- 10 passed\n- 0 failed", "test_agent"),

    # Review phase messages
    ("✅ Starting review phase", "ops"),
    ("✅ Review completed", "reviewer"),

    # Document phase messages
    ("✅ Starting documentation phase", "ops"),
    ("✅ Documentation generated", "documenter"),

    # Patch workflow messages
    ("✅ Starting patch workflow", "ops"),
    ("✅ Patch plan created: specs/patch-123.md", "patch_planner"),
    ("✅ Patch implemented", "patch_implementor"),
]

print("Testing format_issue_message across workflow phases...")
print("=" * 80)

for message, agent in test_messages:
    result = format_issue_message("test123", agent, message)
    print(f"\nOriginal: {message}")
    print(f"Agent:    {agent}")
    print(f"Result:   {result}")

    # Check that exclamation is added correctly
    if message.endswith(("!", "?", ":", ";")):
        # Should not modify messages with existing punctuation
        assert message in result, f"Message was modified when it shouldn't be: {result}"
    elif message.endswith("."):
        # Should replace period with exclamation
        expected = message[:-1] + "!"
        assert expected in result, f"Period not replaced with exclamation: {result}"
    else:
        # Should add exclamation
        expected = message + "!"
        assert expected in result, f"Exclamation not added: {result}"

print("\n" + "=" * 80)
print("✅ All workflow message tests passed!")
print("\nThe exclamation point enhancement is working correctly across all workflow phases!")
print("Messages now have more enthusiasm while preserving existing punctuation rules.")