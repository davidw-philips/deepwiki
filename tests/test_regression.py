"""Regression tests for deepwiki CLI issues.

Tests for:
- Issue #1: UnicodeEncodeError with large documentation containing Unicode characters
- Issue #2: PATH installation and temporary session PATH setup
- Issue #3: JSON argument parsing with improved error messages
"""

import json
import sys
import io
from unittest.mock import patch, MagicMock
import pytest

# Import the functions to test
sys.path.insert(0, str(__file__).replace('\\tests\\test_regression.py', '\\deepwiki'))
from deepwiki.cli import print_result, call_tool, print_help


class TestIssue1UnicodeEncoding:
    """Regression tests for Issue #1: UnicodeEncodeError on Windows with Unicode characters."""

    def test_print_result_with_unicode_characters(self, capsys):
        """Test that print_result handles Unicode characters (→, etc.) without crashing."""
        response = {
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": "This is an arrow → and other Unicode: ✓ ✗ • ◆"
                    }
                ]
            }
        }
        
        # This should not raise UnicodeEncodeError
        print_result(response)
        captured = capsys.readouterr()
        assert "arrow" in captured.out
        assert "Unicode" in captured.out

    def test_print_result_with_large_unicode_documentation(self, capsys):
        """Test handling of large documentation with multiple Unicode characters."""
        # Simulate large documentation with Unicode
        unicode_text = "Architecture Overview → " * 100 + "Special chars: ① ② ③ ④ ⑤"
        response = {
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": unicode_text
                    }
                ]
            }
        }
        
        # Should handle large Unicode text without crashing
        print_result(response)
        captured = capsys.readouterr()
        assert "Architecture" in captured.out

    def test_print_result_with_mixed_content_types(self, capsys):
        """Test print_result with mixed text and non-text content containing Unicode."""
        response = {
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": "Text with Unicode → content"
                    },
                    {
                        "type": "resource",
                        "uri": "file://path/to/resource"
                    }
                ]
            }
        }
        
        print_result(response)
        captured = capsys.readouterr()
        assert "Text with Unicode" in captured.out
        assert "file://path/to/resource" in captured.out


class TestIssue2PathSetup:
    """Regression tests for Issue #2: PATH setup after installation and agent temporary PATH."""

    def test_install_md_exists(self):
        """Test that INSTALL.md file exists with proper guidance."""
        import os
        install_path = os.path.join(os.path.dirname(__file__), '..', 'INSTALL.md')
        assert os.path.exists(install_path), "INSTALL.md should exist"
        
        with open(install_path, 'r') as f:
            content = f.read()
            # Check for key sections
            assert "uv tool update-shell" in content, "Should mention uv tool update-shell"
            assert "export PATH" in content or "$env:PATH" in content, "Should show PATH setup"
            assert "Agents" in content or "agent" in content.lower(), "Should mention agent setup"

    def test_install_md_agent_instructions(self):
        """Test that INSTALL.md includes clear agent temporary PATH instructions."""
        import os
        install_path = os.path.join(os.path.dirname(__file__), '..', 'INSTALL.md')
        
        with open(install_path, 'r') as f:
            content = f.read()
            # Check for Windows PowerShell agent temporary PATH setup
            assert "$env:USERPROFILE" in content or "$env:PATH" in content, \
                "Should include Windows PowerShell PATH setup"
            # Check for Unix agent setup
            assert "$HOME/.local/bin" in content, "Should include Unix PATH setup"
            # Check that it mentions agent context
            assert "agent" in content.lower() and ("editor" in content.lower() or "copilot" in content.lower()), \
                "Should mention agents in editor context"


class TestIssue3JSONParsing:
    """Regression tests for Issue #3: JSON argument parsing with improved error messages."""

    @patch('deepwiki.cli.rpc_request')
    def test_json_parsing_error_with_helpful_message(self, mock_rpc, capsys):
        """Test that JSON parsing errors provide helpful guidance."""
        tools = [{"name": "ask_wiki_question", "description": "Ask about a repo"}]
        
        # Call with invalid JSON
        with pytest.raises(SystemExit) as exc_info:
            call_tool("ask_wiki_question", "{invalid json", tools)
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        
        # Should show error and helpful guidance
        assert "Error parsing JSON arguments" in captured.err
        assert "Expected JSON format" in captured.err or "Example:" in captured.err, \
            "Error message should include helpful format guidance"

    @patch('deepwiki.cli.rpc_request')
    def test_json_parsing_with_valid_json(self, mock_rpc, capsys):
        """Test that valid JSON is accepted correctly."""
        tools = [{"name": "read_wiki_structure", "description": "Get wiki structure"}]
        mock_rpc.return_value = {"result": {"content": [{"type": "text", "text": "Success"}]}}
        
        # Call with valid JSON
        call_tool("read_wiki_structure", '{"repoName":"facebook/react"}', tools)
        
        captured = capsys.readouterr()
        assert "Success" in captured.out
        mock_rpc.assert_called_once()

    @patch('deepwiki.cli.rpc_request')
    def test_json_parsing_error_message_includes_example(self, mock_rpc, capsys):
        """Test that JSON error message includes a concrete example."""
        tools = [{"name": "ask_wiki_question"}]
        
        with pytest.raises(SystemExit):
            call_tool("ask_wiki_question", '{"repoName": "test" invalid}', tools)
        
        captured = capsys.readouterr()
        
        # Should include example usage
        assert "ask_wiki_question" in captured.err or "repoName" in captured.err or "Example" in captured.err, \
            "Error should include example with tool name or JSON keys"

    @patch('deepwiki.cli.rpc_request')
    def test_json_parsing_rejects_non_dict(self, mock_rpc, capsys):
        """Test that non-dict JSON is rejected with helpful error."""
        tools = [{"name": "test_tool"}]
        
        with pytest.raises(SystemExit) as exc_info:
            call_tool("test_tool", '["array", "not", "object"]', tools)
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "JSON object" in captured.err or "dict" in captured.err.lower()


class TestCliIntegration:
    """Integration tests for CLI help and tool information display."""

    def test_print_help_displays_all_tools(self, capsys):
        """Test that print_help correctly displays available tools."""
        tools = [
            {"name": "read_wiki_structure", "description": "Get documentation structure for a repo"},
            {"name": "read_wiki_contents", "description": "Read full documentation"},
            {"name": "ask_wiki_question", "description": "Ask questions about a repository"}
        ]
        
        print_help(tools)
        captured = capsys.readouterr()
        
        for tool in tools:
            assert tool["name"] in captured.out, f"Tool {tool['name']} should appear in help"
            assert tool["description"].split('\n')[0] in captured.out, f"Description should appear in help"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
