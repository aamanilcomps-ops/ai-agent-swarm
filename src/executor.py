import os
import subprocess
from typing import Optional
from src.logger import setup_logger

logger = setup_logger(__name__)


class CodeExecutor:
    """Safe code execution with validation and error handling."""
    
    def __init__(
        self,
        output_dir: str = 'generated_output',
        timeout_seconds: int = 300,
        enable_execution: bool = True
    ):
        """
        Initialize code executor.
        
        Args:
            output_dir: Directory to save generated code
            timeout_seconds: Maximum execution time
            enable_execution: Whether to actually execute code
        """
        self.output_dir = output_dir
        self.timeout_seconds = timeout_seconds
        self.enable_execution = enable_execution
        
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"CodeExecutor initialized with output_dir={output_dir}")
    
    def validate_code(self, code: str) -> bool:
        """
        Basic validation of generated code.
        
        Args:
            code: Python code to validate
        
        Returns:
            True if code appears safe to execute
        """
        dangerous_patterns = [
            'os.system(',
            'subprocess.call(',
            'exec(',
            'eval(',
            '__import__',
            'open(',
            'rm -rf',
            'rm /',
            'dd if=',
            'format c:',
            'mkfs'
        ]
        
        code_lower = code.lower()
        for pattern in dangerous_patterns:
            if pattern in code_lower:
                logger.warning(f"Potentially dangerous pattern detected: {pattern}")
                return False
        
        return True
    
    def save_code(self, code: str, filename: str = 'app.py') -> str:
        """
        Save generated code to file.
        
        Args:
            code: Python code to save
            filename: Output filename
        
        Returns:
            Path to saved file
        """
        file_path = os.path.join(self.output_dir, filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            logger.info(f"Code saved to {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Failed to save code: {e}")
            raise
    
    def execute(self, code: str, filename: str = 'app.py') -> bool:
        """
        Execute generated Python code.
        
        Args:
            code: Python code to execute
            filename: Output filename for the code
        
        Returns:
            True if execution successful, False otherwise
        """
        if not self.enable_execution:
            logger.info("Code execution is disabled")
            return False
        
        # Validate code before execution
        if not self.validate_code(code):
            logger.error("Code validation failed. Execution aborted for safety.")
            return False
        
        # Save code
        file_path = self.save_code(code, filename)
        
        try:
            logger.info(f"⚙️  [Orchestrator] Executing {file_path}")
            print(f"\n⚙️  [Orchestrator] Executing generated code: {file_path}\n")
            
            result = subprocess.run(
                ['python', file_path],
                timeout=self.timeout_seconds,
                capture_output=False,
                check=True
            )
            
            logger.info(f"Code execution completed successfully")
            print(f"\n✅ [Orchestrator] Execution completed successfully\n")
            return True
        
        except subprocess.TimeoutExpired:
            logger.error(f"Code execution timeout after {self.timeout_seconds}s")
            print(f"\n❌ [Orchestrator] Execution timeout after {self.timeout_seconds}s\n")
            return False
        
        except subprocess.CalledProcessError as e:
            logger.error(f"Code execution failed with exit code {e.returncode}")
            print(f"\n❌ [Orchestrator] Execution failed with exit code {e.returncode}\n")
            return False
        
        except Exception as e:
            logger.error(f"Unexpected error during execution: {e}")
            print(f"\n💥 [Orchestrator] Unexpected error: {e}\n")
            return False
    
    def get_status(self) -> dict:
        """Get executor status."""
        return {
            'output_dir': self.output_dir,
            'timeout_seconds': self.timeout_seconds,
            'execution_enabled': self.enable_execution
        }
