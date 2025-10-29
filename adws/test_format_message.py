#!/usr/bin/env python3
"""Simple test script for format_issue_message function."""

# Inline test of the modified function
def format_issue_message(adw_id, agent_name, message, session_id=None):
    """Format a message for issue comments with ADW tracking and bot identifier."""
    ADW_BOT_IDENTIFIER = "[ADW-BOT]"

    # Add exclamation point if message doesn't already end with punctuation
    if message:
        # Check if message ends with punctuation (., !, ?, :, ;)
        if not message.rstrip().endswith(('.', '!', '?', ':', ';')):
            message = message.rstrip() + '!'
        # Replace period with exclamation point for more enthusiasm
        elif message.rstrip().endswith('.'):
            message = message.rstrip()[:-1] + '!'

    # Always include ADW_BOT_IDENTIFIER to prevent webhook loops
    if session_id:
        return f"{ADW_BOT_IDENTIFIER} {adw_id}_{agent_name}_{session_id}: {message}"
    return f"{ADW_BOT_IDENTIFIER} {adw_id}_{agent_name}: {message}"


# Run tests
print("Testing format_issue_message function with exclamation points...")
print("-" * 60)

test_cases = [
    ("Starting process", "Starting process!"),
    ("Process complete!", "Process complete!"),
    ("Ready to proceed?", "Ready to proceed?"),
    ("Process complete.", "Process complete!"),
    ("Results:", "Results:"),
    ("Step 1 done;", "Step 1 done;"),
    ("✅ Process complete", "✅ Process complete!"),
    ("", ""),
    ("  ", "!"),
    ("Process complete  ", "Process complete!"),
]

passed = 0
failed = 0

for input_msg, expected_ending in test_cases:
    result = format_issue_message("test_id", "agent", input_msg)

    # Extract just the message part after the colon
    msg_part = result.split(": ", 1)[1] if ": " in result else ""

    if msg_part == expected_ending:
        print(f"✅ PASS: '{input_msg}' -> '{msg_part}'")
        passed += 1
    else:
        print(f"❌ FAIL: '{input_msg}' -> Got '{msg_part}', Expected '{expected_ending}'")
        failed += 1

print("-" * 60)
print(f"Results: {passed} passed, {failed} failed out of {passed + failed} total")

if failed == 0:
    print("✅ All tests passed! The exclamation point feature is working correctly!")
else:
    print(f"❌ {failed} tests failed. Please review the implementation.")