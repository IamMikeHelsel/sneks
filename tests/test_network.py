import unittest
import pickle
import struct
import io
from snake_game.core.network import send_message, receive_message, HEADER_LENGTH

class MockSocket:
    def __init__(self, initial_buffer=b''):
        self.buffer = io.BytesIO(initial_buffer)
        self.closed = False
        self.name = "mock_socket" # For logging in receive_message

    def sendall(self, data):
        if self.closed:
            raise ConnectionAbortedError("Socket is closed")
        self.buffer.write(data)
        return len(data)

    def recv(self, num_bytes):
        if self.closed:
            raise ConnectionAbortedError("Socket is closed")
        return self.buffer.read(num_bytes)

    def getsockname(self): # Added for compatibility with send_message logging
        return ("mock_host", 12345)
    
    def fileno(self): # Added for compatibility with send_message logging
        return 1 # Dummy file descriptor

    def get_sent_data(self):
        """Helper to get all data written to the send buffer."""
        return self.buffer.getvalue()

    def close(self):
        self.closed = True

class TestNetworkMessaging(unittest.TestCase):

    def test_send_and_receive_simple_dict(self):
        """Test sending and receiving a simple dictionary."""
        mock_sock = MockSocket()
        test_data = {"action": "move", "direction": "UP"}
        
        # Send data
        self.assertTrue(send_message(mock_sock, test_data))
        
        # Prepare for receive by resetting buffer position to start
        mock_sock.buffer.seek(0)
        
        # Receive data
        recv_buffer_map = {'mock_socket': b''}
        received_data = receive_message(mock_sock, recv_buffer_map, 'mock_socket')
        
        self.assertEqual(received_data, test_data)
        self.assertEqual(recv_buffer_map['mock_socket'], b'', "Buffer should be empty after full receive")

    def test_send_and_receive_various_types(self):
        """Test with various Python object types."""
        mock_sock = MockSocket()
        test_cases = [
            {"type": "list", "data": [1, 2, "hello", None]},
            {"type": "int", "data": 12345},
            {"type": "string", "data": "a_long_string_with_various_chars_!@#$%^&*()"},
            {"type": "None", "data": None},
            {"type": "bool", "data": True},
            {"type": "complex_dict", "data": {"players": [{"id": "p1", "score": 10}, {"id": "p2", "score": 5}]}}
        ]
        
        recv_buffer_map = {'mock_socket': b''}
        for case in test_cases:
            mock_sock.buffer = io.BytesIO() # Reset buffer for each send
            
            self.assertTrue(send_message(mock_sock, case["data"]))
            mock_sock.buffer.seek(0) # Reset buffer position for reading
            
            received_data = receive_message(mock_sock, recv_buffer_map, 'mock_socket')
            self.assertEqual(received_data, case["data"], f"Failed for type: {case['type']}")
            self.assertEqual(recv_buffer_map['mock_socket'], b'', "Buffer should be empty")

    def test_receive_partial_header(self):
        """Test receiving data when the header arrives in parts."""
        test_data = {"message": "partial_header_test"}
        pickled_data = pickle.dumps(test_data)
        header = struct.pack('>I', len(pickled_data))
        
        # Simulate receiving only the first 2 bytes of the header
        mock_sock_partial_header = MockSocket(initial_buffer=header[:2])
        recv_buffer_map = {'mock_socket': b''}
        
        # First attempt, should return None as header is incomplete
        msg = receive_message(mock_sock_partial_header, recv_buffer_map, 'mock_socket')
        self.assertIsNone(msg, "Should return None for partial header")
        self.assertEqual(recv_buffer_map['mock_socket'], header[:2], "Buffer should contain partial header")

        # Simulate receiving the rest of the header and the body
        mock_sock_partial_header.buffer.write(header[2:] + pickled_data) # Add rest of header and body
        # No seek(0) here as we are appending to existing buffer content from recv's perspective
        
        msg_complete = receive_message(mock_sock_partial_header, recv_buffer_map, 'mock_socket')
        self.assertEqual(msg_complete, test_data, "Should correctly receive message after header completion")
        self.assertEqual(recv_buffer_map['mock_socket'], b'', "Buffer should be empty after full receive")


    def test_receive_partial_body(self):
        """Test receiving data when the body arrives in parts."""
        test_data = {"message": "partial_body_test_very_long_message_to_ensure_splitting"}
        pickled_data = pickle.dumps(test_data)
        header = struct.pack('>I', len(pickled_data))
        
        # Simulate receiving full header but only part of the body
        body_part1 = pickled_data[:len(pickled_data)//2]
        mock_sock_partial_body = MockSocket(initial_buffer=header + body_part1)
        recv_buffer_map = {'mock_socket': b''}

        # First attempt, should return None as body is incomplete
        msg = receive_message(mock_sock_partial_body, recv_buffer_map, 'mock_socket')
        self.assertIsNone(msg, "Should return None for partial body")
        self.assertEqual(recv_buffer_map['mock_socket'], header + body_part1, "Buffer should contain header and partial body")

        # Simulate receiving the rest of the body
        body_part2 = pickled_data[len(pickled_data)//2:]
        mock_sock_partial_body.buffer.write(body_part2) # Append rest of body
        
        msg_complete = receive_message(mock_sock_partial_body, recv_buffer_map, 'mock_socket')
        self.assertEqual(msg_complete, test_data, "Should correctly receive message after body completion")
        self.assertEqual(recv_buffer_map['mock_socket'], b'', "Buffer should be empty")

    def test_receive_multiple_messages_in_buffer(self):
        """Test receiving when multiple messages are already in the socket's receive buffer."""
        mock_sock = MockSocket()
        data1 = {"id": 1, "content": "message_one"}
        data2 = {"id": 2, "content": "message_two"}

        # Send two messages back-to-back
        send_message(mock_sock, data1)
        send_message(mock_sock, data2)
        
        mock_sock.buffer.seek(0) # Prepare for reading
        recv_buffer_map = {'mock_socket': b''}

        # Receive first message
        received1 = receive_message(mock_sock, recv_buffer_map, 'mock_socket')
        self.assertEqual(received1, data1)
        self.assertNotEqual(recv_buffer_map['mock_socket'], b'', "Buffer should not be empty yet")

        # Receive second message
        received2 = receive_message(mock_sock, recv_buffer_map, 'mock_socket')
        self.assertEqual(received2, data2)
        self.assertEqual(recv_buffer_map['mock_socket'], b'', "Buffer should be empty after all messages received")

    def test_receive_connection_closed_during_header(self):
        """Test when connection is closed while expecting header bytes."""
        mock_sock = MockSocket(initial_buffer=b'\x00') # Incomplete header
        recv_buffer_map = {'mock_socket': b''}
        # Simulate socket closing by making recv return empty bytes
        original_recv = mock_sock.recv
        mock_sock.recv = lambda num_bytes: b'' 
        
        result = receive_message(mock_sock, recv_buffer_map, 'mock_socket')
        self.assertFalse(result, "Should return False on connection closed during header read")
        mock_sock.recv = original_recv # Restore

    def test_receive_connection_closed_during_body(self):
        """Test when connection is closed while expecting body bytes."""
        test_data = {"message": "short"}
        pickled_data = pickle.dumps(test_data)
        header = struct.pack('>I', len(pickled_data))
        
        mock_sock = MockSocket(initial_buffer=header + pickled_data[:2]) # Full header, partial body
        recv_buffer_map = {'mock_socket': b''}
        
        # Attempt to read, buffer what we have
        receive_message(mock_sock, recv_buffer_map, 'mock_socket') 
        
        # Now simulate socket closing for the next recv call
        original_recv = mock_sock.recv
        mock_sock.recv = lambda num_bytes: b''
        
        result = receive_message(mock_sock, recv_buffer_map, 'mock_socket')
        self.assertFalse(result, "Should return False on connection closed during body read")
        mock_sock.recv = original_recv # Restore

    def test_send_on_closed_socket(self):
        """Test that send_message handles a closed socket gracefully."""
        mock_sock = MockSocket()
        mock_sock.close() # Close the socket
        test_data = {"message": "wont_send"}
        
        # send_message should return False and log an error (manual log check)
        self.assertFalse(send_message(mock_sock, test_data))

if __name__ == '__main__':
    unittest.main()
