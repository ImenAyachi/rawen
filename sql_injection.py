import re

def is_sql_injection(input_text):
    # Refined patterns to detect SQL injection attempts more precisely
    patterns = [
        r"(\bselect\b|\binsert\b|\bdelete\b|\bupdate\b|\bdrop\b|\balter\b|\bunion\b|\bexec\b|\b--\b|;|'\s*=\s*1)",  # SQL keywords and suspicious patterns
        r"\b(or|and)\b\s*['\"()=;]",  # Looks for 'or' or 'and' followed by suspicious symbols
        r"'\s*--",  # SQL comment detection
        r"'\s*=\s*1",  # Common injection pattern: 1=1
        r"(\bselect\b|\bupdate\b|\bdelete\b|\binsert\b).*\bfrom\b",  # SELECT/UPDATE/DELETE with FROM
        r"\bunion\b.*\bselect\b",  # UNION SELECT pattern
        r"\bselect\b.*\bwhere\b",  # SELECT ... WHERE pattern
    ]
    
    # Convert the input text to lowercase for easier comparison
    input_lower = input_text.lower()
    
    # Iterate through the patterns and check for matches
    for pattern in patterns:
        if re.search(pattern, input_lower):
            return True
    
    return False
