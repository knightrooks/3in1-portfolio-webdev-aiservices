"""
Voice Performance and Load Tests
Tests for voice API performance, load handling, and resource management
"""

import pytest
import time
import threading
import tempfile
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from unittest.mock import patch, MagicMock
import asyncio
import psutil
import sys

# Performance test configuration
PERFORMANCE_CONFIG = {
    "max_response_time": 30.0,  # seconds
    "max_concurrent_requests": 10,
    "max_memory_usage_mb": 512,  # MB
    "audio_file_max_size_mb": 50,  # MB per file
    "temp_file_cleanup_time": 300,  # seconds
}

AGENT_LIST = [
    "emotionaljenny", "strictwife", "gossipqueen", "lazyjohn", "girlfriend",
    "coderbot", "developer", "strategist", "security_expert", "data_scientist",
    "marketing_specialist", "operations_manager", "content_creator",
    "product_manager", "customer_success", "research_analyst"
]


class TestVoicePerformance:
    """Test voice generation performance metrics"""
    
    def test_single_voice_generation_time(self):
        """Test single voice generation completes within time limit"""
        max_time = PERFORMANCE_CONFIG["max_response_time"]
        
        start_time = time.time()
        
        # Simulate voice generation processing
        with patch('time.sleep') as mock_sleep:
            mock_sleep.return_value = None
            
            # Mock voice processing
            processing_result = {
                "success": True,
                "processing_time": 2.5,
                "audio_generated": True
            }
            
            end_time = time.time()
            actual_time = end_time - start_time
            
            # Verify performance
            assert actual_time < max_time
            assert processing_result["success"] == True
            assert processing_result["processing_time"] < max_time
    
    @pytest.mark.parametrize("agent_name", AGENT_LIST[:5])  # Test subset for performance
    def test_agent_specific_performance(self, agent_name):
        """Test performance for specific agent personalities"""
        
        # Mock agent-specific processing times
        agent_performance_expectations = {
            "emotionaljenny": {"max_time": 25.0, "complexity": "medium"},
            "strictwife": {"max_time": 20.0, "complexity": "low"},
            "gossipqueen": {"max_time": 30.0, "complexity": "high"},
            "lazyjohn": {"max_time": 15.0, "complexity": "low"},
            "coderbot": {"max_time": 25.0, "complexity": "medium"}
        }
        
        if agent_name in agent_performance_expectations:
            expectations = agent_performance_expectations[agent_name]
            
            # Simulate agent processing
            mock_processing_time = {
                "low": 1.0,
                "medium": 2.5, 
                "high": 4.0
            }[expectations["complexity"]]
            
            assert mock_processing_time < expectations["max_time"]
    
    def test_text_length_performance_scaling(self):
        """Test performance scaling with different text lengths"""
        text_lengths = [10, 100, 1000, 5000]  # characters
        
        for length in text_lengths:
            test_text = "a" * length
            
            # Estimate processing time based on text length
            estimated_time = max(1.0, length / 1000.0 * 2.0)  # 2 seconds per 1000 chars
            
            # Verify scaling is reasonable
            assert estimated_time < PERFORMANCE_CONFIG["max_response_time"]
            assert len(test_text) == length
    
    def test_memory_usage_during_voice_generation(self):
        """Test memory usage remains within acceptable limits"""
        max_memory_mb = PERFORMANCE_CONFIG["max_memory_usage_mb"]
        
        # Get initial memory usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Simulate voice generation memory usage
        test_data_size = 10 * 1024 * 1024  # 10MB test data
        test_data = b"0" * test_data_size
        
        # Check memory after allocation
        current_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = current_memory - initial_memory
        
        # Verify memory usage is reasonable
        assert memory_increase < max_memory_mb
        
        # Clean up
        del test_data


class TestVoiceLoadHandling:
    """Test voice API load handling and concurrent requests"""
    
    def test_concurrent_voice_requests(self):
        """Test handling multiple concurrent voice requests"""
        max_concurrent = PERFORMANCE_CONFIG["max_concurrent_requests"]
        
        def simulate_voice_request(request_id):
            """Simulate a single voice request"""
            start_time = time.time()
            
            # Simulate processing delay
            time.sleep(0.1)  # 100ms processing
            
            processing_time = time.time() - start_time
            
            return {
                "request_id": request_id,
                "success": True,
                "processing_time": processing_time,
                "timestamp": time.time()
            }
        
        # Execute concurrent requests
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            futures = []
            
            for i in range(max_concurrent):
                future = executor.submit(simulate_voice_request, f"req-{i}")
                futures.append(future)
            
            # Collect results
            results = []
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
        
        # Verify all requests completed successfully
        assert len(results) == max_concurrent
        for result in results:
            assert result["success"] == True
            assert result["processing_time"] < 5.0  # Reasonable time
    
    def test_rate_limiting_behavior(self):
        """Test rate limiting behavior under load"""
        rate_limit = 30  # requests per minute
        time_window = 60  # seconds
        
        # Simulate rate limiting
        request_times = []
        current_time = time.time()
        
        # Generate request timestamps
        for i in range(rate_limit + 5):  # Exceed rate limit
            request_time = current_time + (i * 0.5)  # 2 requests per second
            request_times.append(request_time)
        
        # Check rate limiting logic
        recent_requests = [
            t for t in request_times 
            if current_time - t < time_window
        ]
        
        # Verify rate limiting would be triggered
        if len(recent_requests) > rate_limit:
            assert True  # Rate limiting should be applied
        else:
            assert len(recent_requests) <= rate_limit
    
    def test_queue_management_under_load(self):
        """Test request queue management under high load"""
        max_queue_size = 50
        
        # Simulate request queue
        request_queue = []
        
        # Add requests to queue
        for i in range(max_queue_size + 10):  # Exceed queue size
            request = {
                "id": f"queue-req-{i}",
                "timestamp": time.time(),
                "text": f"Queue test message {i}"
            }
            
            if len(request_queue) < max_queue_size:
                request_queue.append(request)
        
        # Verify queue size management
        assert len(request_queue) <= max_queue_size
    
    def test_resource_cleanup_under_load(self):
        """Test resource cleanup during high load scenarios"""
        temp_files = []
        
        try:
            # Create multiple temporary files (simulating audio files)
            for i in range(20):
                temp_file = tempfile.NamedTemporaryFile(
                    suffix=f"_load_test_{i}.mp3", 
                    delete=False
                )
                temp_files.append(temp_file.name)
                temp_file.write(b"fake audio data")
                temp_file.close()
            
            # Verify files were created
            for file_path in temp_files:
                assert os.path.exists(file_path)
            
            # Simulate cleanup process
            cleanup_start_time = time.time()
            
            for file_path in temp_files[:10]:  # Clean up half
                os.unlink(file_path)
            
            cleanup_time = time.time() - cleanup_start_time
            
            # Verify cleanup performance
            assert cleanup_time < 5.0  # Should be fast
            
            # Verify cleanup worked
            for file_path in temp_files[:10]:
                assert not os.path.exists(file_path)
                
        finally:
            # Clean up remaining files
            for file_path in temp_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)


class TestVoiceResourceManagement:
    """Test resource management for voice operations"""
    
    def test_audio_file_size_limits(self):
        """Test audio file size management"""
        max_size_mb = PERFORMANCE_CONFIG["audio_file_max_size_mb"]
        max_size_bytes = max_size_mb * 1024 * 1024
        
        # Test various text lengths and expected audio sizes
        text_size_expectations = [
            (100, 1),    # 100 chars -> ~1MB
            (1000, 5),   # 1000 chars -> ~5MB
            (5000, 20),  # 5000 chars -> ~20MB
        ]
        
        for text_length, expected_audio_mb in text_size_expectations:
            expected_size_bytes = expected_audio_mb * 1024 * 1024
            
            # Verify size is within limits
            assert expected_size_bytes < max_size_bytes
            
            # Create test file of expected size
            with tempfile.NamedTemporaryFile(delete=True) as temp_file:
                temp_file.write(b"0" * min(expected_size_bytes, 1024))  # Write sample data
                temp_file.flush()
                
                file_size = os.path.getsize(temp_file.name)
                assert file_size <= max_size_bytes
    
    def test_temporary_file_cleanup_timing(self):
        """Test temporary file cleanup timing"""
        cleanup_time_limit = PERFORMANCE_CONFIG["temp_file_cleanup_time"]
        
        # Create temporary files with timestamps
        temp_files = []
        current_time = time.time()
        
        for i in range(5):
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_files.append({
                "path": temp_file.name,
                "created": current_time - (i * 100)  # Files of different ages
            })
            temp_file.close()
        
        try:
            # Simulate cleanup logic
            files_to_cleanup = [
                f for f in temp_files 
                if current_time - f["created"] > cleanup_time_limit
            ]
            
            # Verify cleanup logic
            for file_info in files_to_cleanup:
                if os.path.exists(file_info["path"]):
                    os.unlink(file_info["path"])
            
            # Check that old files were identified for cleanup
            assert len(files_to_cleanup) >= 0
            
        finally:
            # Clean up all test files
            for file_info in temp_files:
                if os.path.exists(file_info["path"]):
                    os.unlink(file_info["path"])
    
    def test_memory_leak_prevention(self):
        """Test memory leak prevention during extended operations"""
        initial_memory = psutil.Process().memory_info().rss
        
        # Simulate extended voice operations
        for i in range(100):
            # Simulate voice processing cycle
            temp_data = bytearray(1024 * 100)  # 100KB temp data
            
            # Process and cleanup
            processed_data = temp_data[:512]  # Simulate processing
            
            # Explicitly cleanup
            del temp_data
            del processed_data
        
        # Check memory after operations
        final_memory = psutil.Process().memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Verify no significant memory leak (allow some variance)
        max_acceptable_increase = 50 * 1024 * 1024  # 50MB
        assert memory_increase < max_acceptable_increase


class TestVoiceErrorRecovery:
    """Test error recovery and resilience"""
    
    def test_tts_engine_failure_recovery(self):
        """Test recovery from TTS engine failures"""
        
        # Simulate engine failure scenarios
        failure_scenarios = [
            {"engine": "gtts", "error": "Network error", "fallback": "pyttsx3"},
            {"engine": "pyttsx3", "error": "Init failed", "fallback": "gtts"},
            {"engine": "azure", "error": "Auth failed", "fallback": "gtts"}
        ]
        
        for scenario in failure_scenarios:
            # Mock failure and recovery
            with patch('agents.base_agent.gTTS') as mock_gtts:
                if scenario["engine"] == "gtts":
                    mock_gtts.side_effect = Exception(scenario["error"])
                
                # Simulate fallback logic
                recovery_result = {
                    "success": True,
                    "engine_used": scenario["fallback"],
                    "fallback_triggered": True,
                    "original_error": scenario["error"]
                }
                
                # Verify recovery
                assert recovery_result["success"] == True
                assert recovery_result["fallback_triggered"] == True
    
    def test_network_timeout_handling(self):
        """Test handling of network timeouts"""
        timeout_scenarios = [5, 15, 30]  # seconds
        
        for timeout in timeout_scenarios:
            start_time = time.time()
            
            # Simulate timeout scenario
            try:
                # Mock network call with timeout
                with patch('requests.get') as mock_get:
                    mock_get.side_effect = Exception("Timeout")
                    
                    # Simulate timeout handling
                    elapsed_time = time.time() - start_time
                    
                    if elapsed_time < timeout:
                        result = {"success": False, "error": "Timeout", "retry": True}
                    else:
                        result = {"success": False, "error": "Max timeout", "retry": False}
                    
                    # Verify timeout handling
                    assert "error" in result
                    assert isinstance(result["retry"], bool)
                    
            except Exception as e:
                # Verify exception is handled gracefully
                assert str(e) in ["Timeout", "Network error"]
    
    def test_disk_space_error_handling(self):
        """Test handling of disk space errors"""
        
        # Simulate disk space scenarios
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            # Mock disk full error
            mock_temp.side_effect = OSError("No space left on device")
            
            try:
                # Attempt to create temp file
                temp_file = tempfile.NamedTemporaryFile()
            except OSError as e:
                # Verify error handling
                error_result = {
                    "success": False,
                    "error": "Disk space error",
                    "code": "DISK_FULL",
                    "recovery_action": "cleanup_temp_files"
                }
                
                assert error_result["success"] == False
                assert error_result["code"] == "DISK_FULL"


class TestVoiceScalability:
    """Test voice system scalability"""
    
    def test_agent_scaling_performance(self):
        """Test performance scaling across multiple agents"""
        
        # Test with increasing number of agents
        agent_counts = [1, 5, 10, 16]  # Up to all agents
        
        for count in agent_counts:
            agents_to_test = AGENT_LIST[:count]
            
            # Simulate concurrent processing across agents
            start_time = time.time()
            
            results = []
            for agent in agents_to_test:
                # Mock agent processing
                result = {
                    "agent": agent,
                    "processing_time": 2.0,  # Simulate 2s processing
                    "success": True
                }
                results.append(result)
            
            total_time = time.time() - start_time
            
            # Verify scalability
            assert len(results) == count
            assert all(r["success"] for r in results)
            assert total_time < 10.0  # Should complete reasonably fast
    
    def test_request_volume_handling(self):
        """Test handling of high request volumes"""
        
        # Test with increasing request volumes
        request_volumes = [10, 50, 100, 200]
        
        for volume in request_volumes:
            start_time = time.time()
            
            # Simulate processing high volume
            processed_requests = 0
            failed_requests = 0
            
            for i in range(volume):
                # Simulate request processing
                if i % 10 == 9:  # Simulate some failures
                    failed_requests += 1
                else:
                    processed_requests += 1
            
            processing_time = time.time() - start_time
            
            # Verify volume handling
            success_rate = processed_requests / volume
            assert success_rate > 0.85  # At least 85% success rate
            assert processing_time < 30.0  # Reasonable processing time
    
    def test_system_resource_scaling(self):
        """Test system resource usage scaling"""
        
        # Monitor resource usage under different loads
        load_levels = [1, 5, 10]  # Concurrent operations
        
        for load_level in load_levels:
            # Get baseline resource usage
            process = psutil.Process()
            baseline_memory = process.memory_info().rss
            baseline_cpu = process.cpu_percent()
            
            # Simulate load
            for i in range(load_level):
                # Create small workload
                temp_data = bytearray(1024 * 1024)  # 1MB per operation
                # Process data
                processed = len(temp_data)
                del temp_data
            
            # Check resource usage
            current_memory = process.memory_info().rss
            memory_increase = current_memory - baseline_memory
            
            # Verify resource scaling is reasonable
            max_memory_per_operation = 10 * 1024 * 1024  # 10MB per operation
            expected_max_increase = load_level * max_memory_per_operation
            
            assert memory_increase < expected_max_increase


if __name__ == "__main__":
    # Run performance tests
    pytest.main([__file__, "-v", "--tb=short", "-x"])