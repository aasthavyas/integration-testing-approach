"""
This module contains fixtures and tests for integration testing of Docker containers.
"""

from itertools import islice
import re
import time
import subprocess
import pytest

# Define the path to your Docker Compose file
COMPOSE_FILE = 'docker-compose.yml'

# Fixture to start the Docker Compose services
@pytest.fixture(scope='session')
def docker_compose(request):
    """
    Fixture to start the Docker Compose services.

    Args:
        request: Pytest request object.

    Returns:
        str: Path to the Docker Compose file for reuse in other fixtures.
    """
    # Start the services using docker-compose up command
    subprocess.run(['docker-compose', '-f', COMPOSE_FILE, 'up', '-d'], check=True)

    # Wait for the services to initialize
    time.sleep(10)

    # Return the path to the Docker Compose file for reuse in other fixtures
    return COMPOSE_FILE

# Fixture to retrieve logs
@pytest.fixture(scope='session')
def container_logs(docker_compose):
    """
    Fixture to retrieve logs.

    Args:
        docker_compose (str): Path to the Docker Compose file.

    Returns:
        function: A function to retrieve container logs.
    """
    def retrieve_container_logs():
        # Get the logs of the service
        result = subprocess.run(['docker-compose', '-f', docker_compose, 'logs', 'application-container'],
                                capture_output=True, text=True, check=True)
        logs = result.stdout.strip().split('\n')
        # Return the logs for further assertions
        return logs

    return retrieve_container_logs

def is_container_running(docker_compose, container_name):
    """
    Check if a specific container is running.

    Args:
        docker_compose (str): Path to the Docker Compose file.
        container_name (str): Name of the container to check.

    Returns:
        Tuple[bool, List[str]]: A tuple containing a boolean indicating if the container is running
        and a list of all container names.
    """
    # Wait for a reasonable amount of time for containers to start (adjust as needed)
    time.sleep(30)
    
    # Execute the docker-compose ps command to list containers
    result = subprocess.run(['docker-compose', '-f', docker_compose, 'ps', '-a'],
                            capture_output=True, text=True, check=True)
    print(result)
    # Get the standard output from the command
    output = result.stdout

    #  Define a regular expression pattern to extract container names
    container_names = re.findall(r'^\S+', output, re.MULTILINE)[1:]
    return container_name in container_names, container_names

def test_containers_running(docker_compose):
    """
    Test to check if containers are running.

    Args:
        docker_compose (str): Path to the Docker Compose file.
    """
    # Add the container names you want to check
    container_names_to_check = ["integration-testing-approach-application-container-1",
                                "integration-testing-approach-config-container-1"]  
    for container_name in container_names_to_check:
        is_running, all_container_names = is_container_running(docker_compose, container_name)
        assert is_running, f"Container '{container_name}' not found or not running. Containers found: {', '.join(all_container_names)}"

def test_container_logs(container_logs):
    """
    Test to retrieve the logs of the service and check for expected messages.

    Args:
        container_logs (function): Function to retrieve container logs.
    """
    # Retrieve the logs of the service
    # Wait for 5 minutes before checking the log messages
    time.sleep(10)

    logs = container_logs()

    time.sleep(30)

    # Define the expected log messages
    expected_message_one = "Sample"
    expected_message_two = "Configuration:"
    expected_message_three = "Key1: value1"
    expected_message_four = "Key2: value2"

    expected_messages = [
        expected_message_one,
        expected_message_two,
        expected_message_three,
        expected_message_four
    ]

    error_processing_data = "Config Value not found in environment variables."

    error_exceptions_messages = [
        error_processing_data
    ]

    # Check if any of the expected messages are present in the logs
    found_messages = set()
    found_error_messages = set()
    for log in logs:
        for msg in expected_messages:
            if msg in log:
                found_messages.add(msg)
        for error_msg in error_exceptions_messages:
            if error_msg in log:
                found_error_messages.add(log)

    # Check if all expected messages are present in the logs
    missing_messages = set(expected_messages) - found_messages
    # Check if error messages present in logs
    assert not found_error_messages, f"Some error messages found in logs: {', '.join(islice(found_error_messages, 5))}"

    # Check if messages present in the logs if other expected messages are not found
    assert found_messages, f"Some messages not found in logs: {', '.join(missing_messages)}"


# Run the integration tests
if __name__ == '__main__':
    pytest.main([__file__])
