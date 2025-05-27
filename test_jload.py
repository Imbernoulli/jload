import os
import json
import tempfile
import unittest
import shutil
import threading
import time
from jload import jload, jsave, jsave_append

class TestJload(unittest.TestCase):
    """Test suite for jload functionality."""
    
    def setUp(self):
        """Create a temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary directory after tests."""
        shutil.rmtree(self.test_dir)
    
    def write_file(self, filename, content):
        """Helper to write content to a file."""
        with open(os.path.join(self.test_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)
    
    def test_load_json_array(self):
        """Test loading a JSON file with an array of objects."""
        content = '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]'
        self.write_file('array.json', content)
        
        data = jload(os.path.join(self.test_dir, 'array.json'))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Alice')
        self.assertEqual(data[1]['name'], 'Bob')
    
    def test_load_json_single_object(self):
        """Test loading a JSON file with a single object."""
        content = '{"name": "Alice", "age": 30}'
        self.write_file('object.json', content)
        
        data = jload(os.path.join(self.test_dir, 'object.json'))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Alice')
    
    def test_load_jsonl(self):
        """Test loading a JSONL file."""
        content = '{"name": "Alice", "age": 30}\n{"name": "Bob", "age": 25}'
        self.write_file('data.jsonl', content)
        
        data = jload(os.path.join(self.test_dir, 'data.jsonl'))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Alice')
        self.assertEqual(data[1]['name'], 'Bob')
    
    def test_load_empty_file(self):
        """Test loading an empty file."""
        self.write_file('empty.json', '')
        
        data = jload(os.path.join(self.test_dir, 'empty.json'))
        self.assertEqual(data, [])
    
    def test_load_whitespace_only_file(self):
        """Test loading a file with only whitespace."""
        self.write_file('whitespace.json', '   \n   ')
        
        data = jload(os.path.join(self.test_dir, 'whitespace.json'))
        self.assertEqual(data, [])
    
    def test_load_invalid_json(self):
        """Test loading an invalid JSON file."""
        content = '{"name": "Alice", "age": 30'  # Missing closing brace
        self.write_file('invalid.json', content)
        
        with self.assertRaises(ValueError):
            jload(os.path.join(self.test_dir, 'invalid.json'))
    
    def test_load_file_not_found(self):
        """Test loading a non-existent file."""
        with self.assertRaises(FileNotFoundError):
            jload(os.path.join(self.test_dir, 'nonexistent.json'))
    
    def test_load_mixed_jsonl(self):
        """Test loading a JSONL file with some valid and some invalid lines."""
        content = '{"name": "Alice"}\ninvalid line\n{"name": "Bob"}'
        self.write_file('mixed.jsonl', content)
        
        data = jload(os.path.join(self.test_dir, 'mixed.jsonl'))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Alice')
        self.assertEqual(data[1]['name'], 'Bob')
    
    def test_load_jsonl_with_empty_lines(self):
        """Test loading a JSONL file with empty lines."""
        content = '{"name": "Alice"}\n\n{"name": "Bob"}\n'
        self.write_file('empty_lines.jsonl', content)
        
        data = jload(os.path.join(self.test_dir, 'empty_lines.jsonl'))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Alice')
        self.assertEqual(data[1]['name'], 'Bob')
    
    def test_load_non_dictionary_json(self):
        """Test loading a JSON file that doesn't contain dictionaries."""
        content = '[1, 2, 3]'
        self.write_file('numbers.json', content)
        
        with self.assertRaises(ValueError):
            jload(os.path.join(self.test_dir, 'numbers.json'))
    
    def test_load_single_value_json(self):
        """Test loading a JSON file with a single non-object value."""
        content = '"hello"'
        self.write_file('string.json', content)
        
        with self.assertRaises(ValueError):
            jload(os.path.join(self.test_dir, 'string.json'))


class TestJsave(unittest.TestCase):
    """Test suite for jsave functionality."""
    
    def setUp(self):
        """Create a temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary directory after tests."""
        shutil.rmtree(self.test_dir)
    
    def read_file(self, filename):
        """Helper to read content from a file."""
        with open(os.path.join(self.test_dir, filename), 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_save_list_as_json(self):
        """Test saving a list of dictionaries as JSON."""
        data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
        file_path = os.path.join(self.test_dir, 'output.json')
        
        jsave(data, file_path)
        
        # Verify the file was created with correct content
        with open(file_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data, data)
    
    def test_save_dict_as_json(self):
        """Test saving a single dictionary as JSON."""
        data = {'name': 'Alice', 'age': 30}
        file_path = os.path.join(self.test_dir, 'output.json')
        
        jsave(data, file_path)
        
        # Verify the file was created with correct content
        with open(file_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data, data)
    
    def test_save_primitive_as_json(self):
        """Test saving a primitive value as JSON."""
        data = "Hello, world!"
        file_path = os.path.join(self.test_dir, 'output.json')
        
        jsave(data, file_path)
        
        # Verify the file was created with correct content
        with open(file_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data, data)
    
    def test_save_list_as_jsonl(self):
        """Test saving a list of dictionaries as JSONL."""
        data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
        file_path = os.path.join(self.test_dir, 'output.jsonl')
        
        jsave(data, file_path)
        
        # Read the file line by line
        lines = self.read_file('output.jsonl').strip().split('\n')
        self.assertEqual(len(lines), 2)
        
        # Parse each line as JSON
        parsed_data = [json.loads(line) for line in lines]
        self.assertEqual(parsed_data, data)
    
    def test_save_with_custom_format(self):
        """Test saving with explicitly specified format."""
        data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
        
        # Save as JSON despite .jsonl extension
        json_path = os.path.join(self.test_dir, 'output.jsonl')
        jsave(data, json_path, format='json')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        self.assertEqual(json_data, data)
        
        # Save as JSONL despite .json extension
        jsonl_path = os.path.join(self.test_dir, 'output.json')
        jsave(data, jsonl_path, format='jsonl')
        
        lines = self.read_file('output.json').strip().split('\n')
        parsed_data = [json.loads(line) for line in lines]
        self.assertEqual(parsed_data, data)
    
    def test_save_with_custom_indent(self):
        """Test saving JSON with custom indentation."""
        data = {'name': 'Alice', 'age': 30}
        file_path = os.path.join(self.test_dir, 'output.json')
        
        jsave(data, file_path, indent=4)
        
        content = self.read_file('output.json')
        self.assertIn('    "name"', content)  # Should have 4-space indentation
    
    def test_save_non_serializable(self):
        """Test saving non-JSON-serializable data."""
        # Create a circular reference
        data = {'self_ref': None}
        data['self_ref'] = data
        
        file_path = os.path.join(self.test_dir, 'output.json')
        
        try:
            jsave(data, file_path)
            self.fail("Expected an exception for circular reference")
        except Exception as e:
            error_msg = str(e).lower()
            self.assertTrue(
                "circular reference" in error_msg or 
                "not json-serializable" in error_msg or
                "circular" in error_msg
            )
    
    def test_save_non_dict_as_jsonl(self):
        """Test attempting to save non-dictionary items as JSONL."""
        data = [1, 2, 3]  # Not dictionaries
        file_path = os.path.join(self.test_dir, 'output.jsonl')
        
        with self.assertRaises(ValueError):
            jsave(data, file_path)
    
    def test_create_directory_if_not_exists(self):
        """Test that jsave creates directories if they don't exist."""
        data = {'name': 'Alice', 'age': 30}
        nested_path = os.path.join(self.test_dir, 'nested', 'dir', 'output.json')
        
        jsave(data, nested_path)
        
        self.assertTrue(os.path.exists(nested_path))
        with open(nested_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, data)


class TestJsaveAppend(unittest.TestCase):
    """Test suite for jsave append functionality."""
    
    def setUp(self):
        """Create a temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary directory after tests."""
        shutil.rmtree(self.test_dir)
    
    def read_file(self, filename):
        """Helper to read content from a file."""
        with open(os.path.join(self.test_dir, filename), 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_append_to_json_file(self):
        """Test appending to an existing JSON file."""
        # Create initial file
        initial_data = [{'name': 'Alice', 'age': 30}]
        file_path = os.path.join(self.test_dir, 'people.json')
        jsave(initial_data, file_path)
        
        # Append a new entry
        new_entry = {'name': 'Bob', 'age': 25}
        jsave(new_entry, file_path, append=True)
        
        # Verify the file contains both entries
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Alice')
        self.assertEqual(data[1]['name'], 'Bob')
    
    def test_append_to_jsonl_file(self):
        """Test appending to an existing JSONL file."""
        # Create initial file
        initial_data = [{'name': 'Alice', 'age': 30}]
        file_path = os.path.join(self.test_dir, 'people.jsonl')
        jsave(initial_data, file_path)
        
        # Append a new entry
        new_entry = {'name': 'Bob', 'age': 25}
        jsave(new_entry, file_path, append=True)
        
        # Read the file line by line
        lines = self.read_file('people.jsonl').strip().split('\n')
        self.assertEqual(len(lines), 2)
        
        # Parse each line as JSON
        parsed_data = [json.loads(line) for line in lines]
        self.assertEqual(parsed_data[0]['name'], 'Alice')
        self.assertEqual(parsed_data[1]['name'], 'Bob')
    
    def test_append_to_nonexistent_file(self):
        """Test appending to a file that doesn't exist yet."""
        file_path = os.path.join(self.test_dir, 'new_file.json')
        entry = {'name': 'Alice', 'age': 30}
        
        jsave(entry, file_path, append=True)
        
        # Verify the file was created with the entry
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Alice')
    
    def test_append_non_dict(self):
        """Test attempting to append a non-dictionary value."""
        file_path = os.path.join(self.test_dir, 'output.json')
        
        with self.assertRaises(ValueError):
            jsave("Not a dictionary", file_path, append=True)
    
    def test_append_to_non_array_json(self):
        """Test attempting to append to a JSON file that doesn't contain an array."""
        # Create a file with a single object (not an array)
        data = {'name': 'Alice', 'age': 30}
        file_path = os.path.join(self.test_dir, 'person.json')
        jsave(data, file_path)
        
        # Try to append
        new_entry = {'name': 'Bob', 'age': 25}
        
        with self.assertRaises(ValueError):
            jsave(new_entry, file_path, append=True)
    
    def test_jsave_append_function(self):
        """Test the dedicated jsave_append function."""
        file_path = os.path.join(self.test_dir, 'people.json')
        
        # Append to a non-existent file
        entry1 = {'name': 'Alice', 'age': 30}
        jsave_append(entry1, file_path)
        
        # Append to the now-existing file
        entry2 = {'name': 'Bob', 'age': 25}
        jsave_append(entry2, file_path)
        
        # Verify the file contains both entries
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Alice')
        self.assertEqual(data[1]['name'], 'Bob')
    
    def test_concurrent_appends(self):
        """Test concurrent appends from multiple threads."""
        file_path = os.path.join(self.test_dir, 'concurrent.jsonl')
        num_threads = 5
        entries_per_thread = 10
        
        def append_entries():
            for i in range(entries_per_thread):
                entry = {'thread_id': threading.current_thread().name, 'count': i}
                jsave_append(entry, file_path, format='jsonl')
                time.sleep(0.01)  # Small delay to increase chance of concurrency
        
        # Start multiple threads that append to the same file
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=append_entries, name=f"Thread-{i}")
            threads.append(t)
            t.start()
        
        # Wait for all threads to complete
        for t in threads:
            t.join()
        
        # Read the file and verify all entries were written
        lines = self.read_file('concurrent.jsonl').strip().split('\n')
        self.assertEqual(len(lines), num_threads * entries_per_thread)
        
        # Parse and count entries from each thread
        parsed_data = [json.loads(line) for line in lines]
        thread_counts = {}
        
        for entry in parsed_data:
            thread_id = entry['thread_id']
            if thread_id not in thread_counts:
                thread_counts[thread_id] = 0
            thread_counts[thread_id] += 1
        
        # Verify each thread wrote the correct number of entries
        for i in range(num_threads):
            thread_name = f"Thread-{i}"
            self.assertEqual(thread_counts.get(thread_name, 0), entries_per_thread)


if __name__ == '__main__':
    unittest.main()