"""Unit tests for workflow_ops.py format_issue_message function."""

import sys
import os
# Add parent directory to path to import adw_modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adw_modules.workflow_ops import format_issue_message


class TestFormatIssueMessage:
    """Test the format_issue_message function with exclamation point enhancement."""

    def test_message_without_punctuation(self):
        """Test messages without punctuation get exclamation point added."""
        result = format_issue_message("test_id", "agent", "Starting process")
        assert result.endswith("Starting process!")
        assert "[ADW-BOT]" in result

    def test_message_already_with_exclamation(self):
        """Test messages already ending with ! are not modified."""
        result = format_issue_message("test_id", "agent", "Process complete!")
        assert result.endswith("Process complete!")
        assert "[ADW-BOT]" in result
        # Should not have double exclamation
        assert not result.endswith("!!")

    def test_message_with_question_mark(self):
        """Test messages ending with ? are not modified."""
        result = format_issue_message("test_id", "agent", "Ready to proceed?")
        assert result.endswith("Ready to proceed?")
        assert not result.endswith("?!")
        assert "[ADW-BOT]" in result

    def test_message_with_period(self):
        """Test messages ending with . get period replaced with !."""
        result = format_issue_message("test_id", "agent", "Process complete.")
        assert result.endswith("Process complete!")
        assert not result.endswith(".!")
        assert "[ADW-BOT]" in result

    def test_message_with_colon(self):
        """Test messages ending with : are not modified."""
        result = format_issue_message("test_id", "agent", "Results:")
        assert result.endswith("Results:")
        assert not result.endswith(":!")
        assert "[ADW-BOT]" in result

    def test_message_with_semicolon(self):
        """Test messages ending with ; are not modified."""
        result = format_issue_message("test_id", "agent", "Step 1 done;")
        assert result.endswith("Step 1 done;")
        assert not result.endswith(";!")
        assert "[ADW-BOT]" in result

    def test_message_with_emoji_at_end(self):
        """Test messages ending with emoji get exclamation point added."""
        result = format_issue_message("test_id", "agent", "✅ Process complete")
        assert result.endswith("✅ Process complete!")
        assert "[ADW-BOT]" in result

    def test_empty_message(self):
        """Test empty messages are handled gracefully."""
        result = format_issue_message("test_id", "agent", "")
        assert "[ADW-BOT]" in result
        assert "test_id_agent:" in result

    def test_whitespace_only_message(self):
        """Test whitespace-only messages are handled correctly."""
        result = format_issue_message("test_id", "agent", "  ")
        assert "[ADW-BOT]" in result
        # Whitespace should be trimmed and exclamation added
        assert "test_id_agent: !" in result

    def test_message_with_trailing_whitespace(self):
        """Test messages with trailing whitespace are trimmed before punctuation check."""
        result = format_issue_message("test_id", "agent", "Process complete  ")
        assert "Process complete!" in result
        assert not "Process complete  !" in result
        assert "[ADW-BOT]" in result

    def test_multiline_message(self):
        """Test multiline messages get exclamation at the end."""
        message = "Line 1\nLine 2\nLine 3"
        result = format_issue_message("test_id", "agent", message)
        assert result.endswith("Line 3!")
        assert "[ADW-BOT]" in result

    def test_message_with_session_id(self):
        """Test messages with session_id include it in format."""
        result = format_issue_message("test_id", "agent", "Process running", "session123")
        assert "test_id_agent_session123:" in result
        assert result.endswith("Process running!")
        assert "[ADW-BOT]" in result

    def test_bot_identifier_always_present(self):
        """Test ADW_BOT_IDENTIFIER is always included."""
        result = format_issue_message("test_id", "agent", "Any message")
        assert "[ADW-BOT]" in result

    def test_json_block_in_message(self):
        """Test messages with JSON blocks get exclamation at the end."""
        message = 'Status update\n```json\n{"status": "ok"}\n```'
        result = format_issue_message("test_id", "agent", message)
        # Should add exclamation after the closing backticks
        assert result.endswith('```!')
        assert "[ADW-BOT]" in result


# Run tests directly
if __name__ == "__main__":
    test = TestFormatIssueMessage()
    test_methods = [method for method in dir(test) if method.startswith('test_')]

    print("Running tests for format_issue_message function...")
    print("-" * 60)

    passed = 0
    failed = 0

    for method_name in test_methods:
        try:
            method = getattr(test, method_name)
            method()
            print(f"✅ {method_name}: PASSED")
            passed += 1
        except AssertionError as e:
            print(f"❌ {method_name}: FAILED - {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {method_name}: ERROR - {e}")
            failed += 1

    print("-" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {passed + failed} total")
    if failed == 0:
        print("✅ All tests passed!")