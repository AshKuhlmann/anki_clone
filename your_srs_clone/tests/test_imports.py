import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def test_import_your_srs_clone():
    """Test that the your_srs_clone package can be imported."""
    try:
        import your_srs_clone
        assert your_srs_clone is not None, "your_srs_clone should be importable"
        print("Successfully imported your_srs_clone")
    except ImportError as e:
        print(f"Failed to import your_srs_clone: {e}")
        assert False, "your_srs_clone failed to import"

if __name__ == "__main__":
    test_import_your_srs_clone()