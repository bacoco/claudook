#!/usr/bin/env python3
"""
Claude Hook - Documentation Enforcer
Ensures all functions have proper documentation.
"""
import json
import sys
import re
import os

def load_hook_data():
    """Load and parse hook data from stdin."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}

def find_undocumented_python_functions(content):
    """Find Python functions without docstrings."""
    undocumented = []
    
    # Find all function definitions
    function_pattern = r'def\s+(\w+)\s*\([^)]*\):'
    functions = re.findall(function_pattern, content)
    
    for func in functions:
        # Skip private functions (starting with _)
        if func.startswith('_'):
            continue
            
        # Look for docstring after function definition
        func_def_pattern = rf'def\s+{re.escape(func)}\s*\([^)]*\):\s*"""'
        if not re.search(func_def_pattern, content, re.DOTALL):
            # Also check for single quotes docstring
            func_def_pattern_single = rf'def\s+{re.escape(func)}\s*\([^)]*\):\s*\'\'\''
            if not re.search(func_def_pattern_single, content, re.DOTALL):
                undocumented.append(func)
    
    return undocumented

def find_undocumented_js_functions(content):
    """Find JavaScript/TypeScript functions without JSDoc."""
    undocumented = []
    
    # Function declaration patterns
    patterns = [
        r'function\s+(\w+)\s*\(',
        r'(\w+)\s*:\s*function\s*\(',
        r'(\w+)\s*=\s*function\s*\(',
        r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>',
        r'(\w+)\s*:\s*\([^)]*\)\s*=>',
    ]
    
    for pattern in patterns:
        functions = re.findall(pattern, content)
        for func in functions:
            if func and not func.startswith('_'):
                # Look for JSDoc comment before function
                jsdoc_pattern = rf'/\*\*.*?\*/\s*.*?{re.escape(func)}'
                if not re.search(jsdoc_pattern, content, re.DOTALL):
                    undocumented.append(func)
    
    return list(set(undocumented))  # Remove duplicates

def find_undocumented_go_functions(content):
    """Find Go functions without comments."""
    undocumented = []
    
    # Find Go function definitions  
    function_pattern = r'func\s+(\w+)\s*\('
    functions = re.findall(function_pattern, content)
    
    for func in functions:
        # Skip private functions (lowercase first letter in Go)
        if func[0].islower():
            continue
            
        # Look for Go-style comment
        comment_pattern = rf'//\s+{re.escape(func)}.*?\nfunc\s+{re.escape(func)}'
        if not re.search(comment_pattern, content, re.DOTALL):
            undocumented.append(func)
    
    return undocumented

def find_undocumented_java_methods(content):
    """Find Java methods without Javadoc."""
    undocumented = []
    
    # Find Java method definitions
    method_pattern = r'(?:public|private|protected)\s+(?:static\s+)?\w+\s+(\w+)\s*\('
    methods = re.findall(method_pattern, content)
    
    for method in methods:
        # Skip constructors and common methods
        if method in ['main', 'toString', 'equals', 'hashCode']:
            continue
            
        # Look for Javadoc
        javadoc_pattern = rf'/\*\*.*?\*/\s*(?:public|private|protected).*?{re.escape(method)}'
        if not re.search(javadoc_pattern, content, re.DOTALL):
            undocumented.append(method)
    
    return undocumented

def find_undocumented_functions(file_path, content):
    """Find undocumented functions based on file extension."""
    if not content:
        return []
    
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.py':
        return find_undocumented_python_functions(content)
    elif file_extension in ['.js', '.ts', '.jsx', '.tsx']:
        return find_undocumented_js_functions(content)
    elif file_extension == '.go':
        return find_undocumented_go_functions(content)
    elif file_extension == '.java':
        return find_undocumented_java_methods(content)
    
    return []

def get_documentation_requirements(file_extension):
    """Get documentation requirements for file type."""
    
    requirements = {
        '.py': [
            '✓ Python docstrings with """triple quotes"""',
            '✓ Parameter descriptions with types (Args: param (type): description)',
            '✓ Return value documentation (Returns: type: description)', 
            '✓ Example usage for complex functions (Examples: >>> func(args))',
            '✓ Exception documentation if applicable (Raises: ExceptionType: description)'
        ],
        '.js': [
            '✓ JSDoc comments with /** */',
            '✓ @param {type} name - description for parameters',
            '✓ @returns {type} description for return values',
            '✓ @example for complex functions',
            '✓ @throws {Error} for exceptions'
        ],
        '.ts': [
            '✓ JSDoc comments with /** */',
            '✓ @param name - description (types from TypeScript)',
            '✓ @returns description (types from TypeScript)',
            '✓ @example for complex functions',
            '✓ @throws for exceptions'
        ],
        '.jsx': [
            '✓ JSDoc comments with /** */',
            '✓ @param {Object} props - component props',
            '✓ @returns {JSX.Element} component description',
            '✓ @example usage examples',
            '✓ Component purpose and behavior'
        ],
        '.tsx': [
            '✓ JSDoc comments with /** */',
            '✓ @param props - component props (typed)',
            '✓ @returns component description',
            '✓ @example usage examples',
            '✓ Component purpose and behavior'
        ],
        '.go': [
            '✓ Go-style comments starting with function name',
            '✓ Parameter descriptions',
            '✓ Return value descriptions',
            '✓ Usage examples for public functions',
            '✓ Error return documentation'
        ],
        '.java': [
            '✓ Javadoc comments with /** */',
            '✓ @param tags for all parameters',
            '✓ @return tag for return values',
            '✓ @throws tags for exceptions',
            '✓ Method purpose and behavior'
        ]
    }
    
    return requirements.get(file_extension, [
        '✓ Appropriate documentation for the language',
        '✓ Parameter and return value descriptions',
        '✓ Usage examples where helpful'
    ])

def create_documentation_message(file_path, undocumented, file_extension):
    """Create documentation enforcement message."""
    
    requirements = get_documentation_requirements(file_extension)
    
    # Determine language name
    language_names = {
        '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
        '.jsx': 'React JSX', '.tsx': 'React TypeScript',
        '.go': 'Go', '.java': 'Java'
    }
    
    language = language_names.get(file_extension, 'code')
    
    return f"""📚 DOCUMENTATION REQUIRED for {file_path}

🚫 UNDOCUMENTED FUNCTIONS DETECTED

Functions missing documentation:
{', '.join(undocumented[:8])}{'...' if len(undocumented) > 8 else ''}

📊 Total undocumented: {len(undocumented)} functions

🎯 {language} Documentation Requirements:

{chr(10).join(requirements)}

💡 Documentation Benefits:
• Improved code maintainability
• Easier onboarding for team members  
• Better IDE support and autocomplete
• Reduced debugging time
• Professional code standards

🚫 You cannot proceed without proper documentation.

💡 Tip: Start with the most critical/public functions first.
"""

def should_check_documentation(file_path, content):
    """Determine if file should be checked for documentation."""
    
    if not file_path or not content:
        return False
    
    # Skip small files (likely not worth documenting)
    if len(content) < 100:
        return False
    
    # Skip test files
    if any(pattern in file_path.lower() for pattern in ['test', 'spec', '__test__']):
        return False
    
    # Skip configuration files
    config_patterns = ['.config.', 'webpack.', 'babel.', 'jest.', 'eslint.']
    if any(pattern in file_path for pattern in config_patterns):
        return False
    
    return True

def main():
    """Main documentation enforcer logic."""
    data = load_hook_data()
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    content = tool_input.get("content", "")
    
    # Only process Write operations (new files with content)
    if tool_name != "Write":
        sys.exit(0)
    
    if not should_check_documentation(file_path, content):
        sys.exit(0)
    
    # Check for supported file extensions
    file_extension = os.path.splitext(file_path)[1].lower()
    supported_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.java']
    
    if file_extension not in supported_extensions:
        sys.exit(0)
    
    # Find undocumented functions
    undocumented = find_undocumented_functions(file_path, content)
    
    if not undocumented:
        # All functions are documented, allow the operation
        sys.exit(0)
    
    # Block and require documentation
    documentation_message = create_documentation_message(file_path, undocumented, file_extension)
    
    output = {
        "decision": "block",
        "reason": documentation_message
    }
    
    print(json.dumps(output))
    sys.exit(2)

if __name__ == "__main__":
    main()
