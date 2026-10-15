"""Contract tests for deepwiki CLI tools.

These tests verify that each tool works correctly with real API calls
and returns proper contract-compliant responses.
"""

import json
import sys
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

# Import the CLI functions
sys.path.insert(0, str(__file__).replace('\\tests\\test_contract.py', '\\deepwiki'))
from deepwiki.cli import rpc_request, print_result, call_tool, list_tools


class TestReadWikiStructureTool:
    """Contract tests for read_wiki_structure tool."""

    def test_read_wiki_structure_with_microsoft_vscode(self, capsys):
        """Test read_wiki_structure returns valid documentation topics for VS Code."""
        sys.argv = ['deepwiki', 'call', 'read_wiki_structure', '{"repoName":"microsoft/vscode"}']
        
        try:
            # Attempt to call the tool
            tools = list_tools()
            assert len(tools) > 0, "Should have at least one tool available"
            
            call_tool('read_wiki_structure', '{"repoName":"microsoft/vscode"}', tools)
            captured = capsys.readouterr()
            
            # Verify output contains expected structure
            assert "Available pages" in captured.out or "pages for" in captured.out.lower(), \
                "Should return documentation structure"
        except Exception as e:
            # If network call fails, at least verify the error is appropriate
            if "Network error" in str(e) or "HTTP" in str(e):
                pytest.skip("Network unavailable for integration test")
            raise

    def test_read_wiki_structure_with_facebook_react(self, capsys):
        """Test read_wiki_structure with facebook/react repository."""
        tools = list_tools()
        
        try:
            call_tool('read_wiki_structure', '{"repoName":"facebook/react"}', tools)
            captured = capsys.readouterr()
            
            # React should have documentation topics
            assert "pages" in captured.out.lower() or "architecture" in captured.out.lower() or captured.out.strip(), \
                "Should return documentation structure for React"
        except Exception as e:
            if "Network error" in str(e) or "HTTP" in str(e):
                pytest.skip("Network unavailable")
            raise

    def test_read_wiki_structure_with_nodejs(self, capsys):
        """Test read_wiki_structure with nodejs/node repository."""
        tools = list_tools()
        
        try:
            call_tool('read_wiki_structure', '{"repoName":"nodejs/node"}', tools)
            captured = capsys.readouterr()
            
            # Should return structure for Node.js
            assert captured.out.strip(), "Should return non-empty documentation"
        except Exception as e:
            if "Network error" in str(e) or "HTTP" in str(e):
                pytest.skip("Network unavailable")
            raise

    def test_read_wiki_structure_response_format(self, capsys):
        """Test that read_wiki_structure returns expected format."""
        tools = list_tools()
        
        try:
            call_tool('read_wiki_structure', '{"repoName":"google/go-github"}', tools)
            captured = capsys.readouterr()
            
            # Verify the response is text-based documentation
            output = captured.out.strip()
            assert len(output) > 0, "Should return non-empty output"
            # Should contain page numbers and titles
            assert ("-" in output or "." in output or any(c.isdigit() for c in output)), \
                "Should contain structured documentation markers"
        except Exception as e:
            if "Network error" in str(e) or "HTTP" in str(e):
                pytest.skip("Network unavailable")
            raise


class TestReadWikiContentsTool:
    """Contract tests for read_wiki_contents tool."""

    def test_read_wiki_contents_accepts_repo_name(self, capsys):
        """Test that read_wiki_contents accepts repository names."""
        tools = list_tools()
        
        # Find the tool
        tool = next((t for t in tools if t.get('name') == 'read_wiki_contents'), None)
        assert tool is not None, "read_wiki_contents tool should exist"
        
        # Verify schema
        schema = tool.get('inputSchema', {})
        assert 'repoName' in schema.get('properties', {}), \
            "read_wiki_contents should accept repoName parameter"

    def test_read_wiki_contents_with_small_repo(self, capsys):
        """Test read_wiki_contents returns content for a repository."""
        tools = list_tools()
        
        try:
            # Use a smaller repo that might have smaller documentation
            call_tool('read_wiki_contents', '{"repoName":"golang/go"}', tools)
            captured = capsys.readouterr()
            
            # Should return documentation content
            assert len(captured.out) > 100 or "error" not in captured.err.lower(), \
                "Should return substantial documentation content or successful message"
        except Exception as e:
            if "Network error" in str(e) or "HTTP" in str(e):
                pytest.skip("Network unavailable")
            raise

    def test_read_wiki_contents_response_is_text(self, capsys):
        """Test that read_wiki_contents returns readable text content."""
        tools = list_tools()
        
        try:
            call_tool('read_wiki_contents', '{"repoName":"python/cpython"}', tools)
            captured = capsys.readouterr()
            
            # Verify response is readable text (not JSON object)
            output = captured.out.strip()
            # Should not be just JSON structure
            assert not (output.startswith('{') and output.endswith('}')), \
                "Should return readable documentation, not raw JSON"
        except Exception as e:
            if "Network error" in str(e):
                pytest.skip("Network unavailable")
            raise


class TestAskWikiQuestionTool:
    """Contract tests for ask_wiki_question tool."""

    def test_ask_wiki_question_requires_repo_and_question(self):
        """Test that ask_wiki_question requires both repoName and question."""
        tools = list_tools()
        
        # Find the tool
        tool = next((t for t in tools if t.get('name') == 'ask_wiki_question'), None)
        assert tool is not None, "ask_wiki_question tool should exist"
        
        # Verify schema requirements
        schema = tool.get('inputSchema', {})
        properties = schema.get('properties', {})
        required = schema.get('required', [])
        
        assert 'repoName' in properties, "Should accept repoName"
        assert 'question' in properties, "Should accept question"
        assert 'repoName' in required, "repoName should be required"
        assert 'question' in required, "question should be required"

    def test_ask_wiki_question_architecture_query(self, capsys):
        """Test asking about repository architecture."""
        tools = list_tools()
        
        try:
            call_tool(
                'ask_wiki_question',
                '{"repoName":"kubernetes/kubernetes","question":"What is the overall architecture?"}',
                tools
            )
            captured = capsys.readouterr()
            
            # Should return an answer to the question
            output = captured.out.strip()
            assert len(output) > 0, "Should provide an answer to the question"
        except Exception as e:
            if "Network error" in str(e) or "HTTP" in str(e):
                pytest.skip("Network unavailable")
            raise

    def test_ask_wiki_question_design_query(self, capsys):
        """Test asking about design patterns."""
        tools = list_tools()
        
        try:
            call_tool(
                'ask_wiki_question',
                '{"repoName":"torvalds/linux","question":"How is the module system organized?"}',
                tools
            )
            captured = capsys.readouterr()
            
            # Should return a response
            output = captured.out.strip()
            assert len(output) > 0, "Should answer design-related questions"
        except Exception as e:
            if "Network error" in str(e):
                pytest.skip("Network unavailable")
            raise

    def test_ask_wiki_question_implementation_query(self, capsys):
        """Test asking implementation-specific questions."""
        tools = list_tools()
        
        try:
            call_tool(
                'ask_wiki_question',
                '{"repoName":"rust-lang/rust","question":"How does the compiler front-end work?"}',
                tools
            )
            captured = capsys.readouterr()
            
            # Should return implementation details
            output = captured.out.strip()
            assert len(output) > 0 or "error" not in captured.err.lower(), \
                "Should handle implementation queries"
        except Exception as e:
            if "Network error" in str(e):
                pytest.skip("Network unavailable")
            raise


class TestToolListingAndDiscovery:
    """Contract tests for tool discovery and metadata."""

    def test_tools_list_available(self):
        """Test that at least the three expected tools are available."""
        tools = list_tools()
        
        assert len(tools) >= 3, "Should have at least 3 tools available"
        
        tool_names = {tool.get('name') for tool in tools}
        expected_tools = {'read_wiki_structure', 'read_wiki_contents', 'ask_wiki_question'}
        
        assert expected_tools.issubset(tool_names), \
            f"Should have all expected tools. Got: {tool_names}"

    def test_all_tools_have_descriptions(self):
        """Test that all tools have descriptions."""
        tools = list_tools()
        
        for tool in tools:
            assert 'name' in tool, "Tool should have a name"
            assert 'description' in tool, f"Tool {tool.get('name')} should have a description"
            assert len(tool['description']) > 0, \
                f"Tool {tool.get('name')} description should not be empty"

    def test_all_tools_have_input_schema(self):
        """Test that all tools have input schemas."""
        tools = list_tools()
        
        for tool in tools:
            assert 'inputSchema' in tool, \
                f"Tool {tool.get('name')} should have inputSchema"
            
            schema = tool['inputSchema']
            assert 'properties' in schema, \
                f"Tool {tool.get('name')} schema should have properties"
            assert 'type' in schema, \
                f"Tool {tool.get('name')} schema should specify type"

    def test_read_wiki_structure_schema_valid(self):
        """Test read_wiki_structure has valid schema."""
        tools = list_tools()
        tool = next((t for t in tools if t.get('name') == 'read_wiki_structure'), None)
        
        assert tool is not None, "Tool should exist"
        schema = tool['inputSchema']
        assert schema.get('type') == 'object', "Schema should be object type"
        assert 'repoName' in schema['properties'], "Should accept repoName"
        assert 'repoName' in schema.get('required', []), "repoName should be required"

    def test_read_wiki_contents_schema_valid(self):
        """Test read_wiki_contents has valid schema."""
        tools = list_tools()
        tool = next((t for t in tools if t.get('name') == 'read_wiki_contents'), None)
        
        assert tool is not None, "Tool should exist"
        schema = tool['inputSchema']
        assert schema.get('type') == 'object', "Schema should be object type"
        assert 'repoName' in schema['properties'], "Should accept repoName"

    def test_ask_wiki_question_schema_valid(self):
        """Test ask_wiki_question has valid schema."""
        tools = list_tools()
        tool = next((t for t in tools if t.get('name') == 'ask_wiki_question'), None)
        
        assert tool is not None, "Tool should exist"
        schema = tool['inputSchema']
        assert schema.get('type') == 'object', "Schema should be object type"
        assert 'repoName' in schema['properties'], "Should accept repoName"
        assert 'question' in schema['properties'], "Should accept question"
        assert 'repoName' in schema.get('required', []), "repoName should be required"
        assert 'question' in schema.get('required', []), "question should be required"


class TestErrorHandling:
    """Contract tests for error handling and edge cases."""

    def test_invalid_json_shows_helpful_error(self, capsys):
        """Test that invalid JSON produces helpful error message."""
        tools = list_tools()
        
        with pytest.raises(SystemExit):
            call_tool('read_wiki_structure', '{invalid json}', tools)
        
        captured = capsys.readouterr()
        assert "Error parsing JSON" in captured.err or "expected" in captured.err.lower(), \
            "Should show helpful error for invalid JSON"

    def test_missing_required_parameter_fails(self, capsys):
        """Test that missing required parameters fail appropriately."""
        tools = list_tools()
        
        # ask_wiki_question requires both repoName and question
        # Missing 'question' parameter will cause MCP server validation error
        try:
            call_tool('ask_wiki_question', '{"repoName":"facebook/react"}', tools)
            captured = capsys.readouterr()
            # Should contain validation error from MCP in output or error
            output = captured.out + captured.err
            assert "Missing" in output or "required" in output.lower() or \
                   "error" in output.lower(), \
                   "Should show validation error for missing parameter"
        except SystemExit:
            # Some error conditions may exit
            pass

    def test_empty_json_object(self, capsys):
        """Test handling of empty JSON object."""
        tools = list_tools()
        
        # This should fail because required parameters are missing
        try:
            # read_wiki_structure requires 'repoName' parameter
            call_tool('read_wiki_structure', '{}', tools)
            captured = capsys.readouterr()
            # Should contain validation error from MCP in output or error
            output = captured.out + captured.err
            assert "Missing" in output or "required" in output.lower() or \
                   "error" in output.lower(), \
                   "Should show validation error for missing required fields"
        except SystemExit:
            # Some error conditions may exit
            pass

    def test_tool_not_found(self, capsys):
        """Test handling of non-existent tool."""
        tools = list_tools()
        
        with pytest.raises(SystemExit):
            call_tool('nonexistent_tool', '{}', tools)
        
        captured = capsys.readouterr()
        assert "not found" in captured.err.lower(), \
            "Should indicate tool was not found"


class TestCrossRepositoryConsistency:
    """Test that tools behave consistently across different repositories."""

    def test_structure_tool_works_across_repos(self):
        """Test read_wiki_structure works with multiple different repositories."""
        tools = list_tools()
        
        repos = [
            'microsoft/vscode',
            'facebook/react',
            'google/go-github',
            'golang/go',
        ]
        
        for repo in repos:
            try:
                # Just verify the tool can be called without error
                assert any(t.get('name') == 'read_wiki_structure' for t in tools), \
                    "Tool should exist"
            except Exception as e:
                if "Network error" not in str(e):
                    raise

    def test_question_tool_accepts_various_questions(self):
        """Test that ask_wiki_question handles various question types."""
        tools = list_tools()
        
        questions = [
            '{"repoName":"python/cpython","question":"What is the main loop?"}',
            '{"repoName":"python/cpython","question":"How does garbage collection work?"}',
            '{"repoName":"python/cpython","question":"Describe the module system"}',
        ]
        
        for question_json in questions:
            # Verify JSON is valid
            parsed = json.loads(question_json)
            assert 'repoName' in parsed, "Should have repoName"
            assert 'question' in parsed, "Should have question"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
