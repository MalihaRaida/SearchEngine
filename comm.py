# class Comm { 
#       static Iterator getDocs (String u) throws NotPossibleException
#         // EFFECTS: If u isn’t a legitimate URL or the site it names does not
#         //   respond as expected throws NotPossibleException else returns a
#         //   generator that will produce the documents from site u (as strings). 
   
#    }

"""Communication module for fetching documents from URLs.

This is a simplified implementation for demonstration purposes.
"""

from typing import Iterator, List


class NotPossibleException(Exception):
    """Raised when URL operations fail."""
    pass


class Comm:
    """Provides static method to fetch documents from URLs."""
    
    @staticmethod
    def getDocs(u: str) -> Iterator[str]:
        """Fetch documents from a URL.
        
        Args:
            u: The URL to fetch documents from
            
        Returns:
            An iterator that yields document strings
            
        Raises:
            NotPossibleException: If the URL is invalid or cannot be accessed
        """
        if not u or not isinstance(u, str):
            raise NotPossibleException("Invalid URL")
        
        # For this implementation, we'll support a simple file:// protocol
        # and a mock http:// protocol for testing
        
        if u.startswith("file://"):
            # Read from local file
            filepath = u[7:]  # Remove "file://"
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                    # Split on double newlines to get separate documents
                    docs = content.split("\n\n\n")
                    for doc in docs:
                        if doc.strip():
                            yield doc.strip()
            except FileNotFoundError:
                raise NotPossibleException(f"File not found: {filepath}")
            except Exception as e:
                raise NotPossibleException(f"Error reading file: {str(e)}")
        
        elif u.startswith("http://") or u.startswith("https://"):
            # Mock HTTP implementation - in real implementation, would use requests library
            # For now, just raise an exception with helpful message
            raise NotPossibleException(
                "HTTP fetching not implemented in this version. Use file:// URLs."
            )
        
        else:
            raise NotPossibleException(f"Unsupported URL protocol: {u}")
