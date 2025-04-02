# main.py - My implementation of an AI-enhanced CI/CD pipeline
# Built this to showcase for Marqeta interview - combines AWS, Python, and AI

import os
import json
import logging
import requests
from datetime import datetime
from typing import Dict, List, Any

# Importing my custom modules for each pipeline component
from modules.code_analysis import CodeAnalyzer
from modules.test_manager import TestManager
from modules.deployment_manager import DeploymentManager
from modules.security_scanner import SecurityScanner
from modules.ai_assistant import AIAssistant

# Setting up basic logging - might want to improve this later with a custom formatter
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AICICDPipeline:
    """
    My implementation of an AI-enhanced CI/CD pipeline that uses LLMs to make smarter
    decisions about code quality, security risks, and deployment safety.
    
    I built this because traditional pipelines rely too much on static rules
    and don't use context when making decisions.
    """
    
    def __init__(self, repo_url: str, branch: str, aws_region: str = 'us-west-2'):
        self.repo_url = repo_url
        self.branch = branch
        self.aws_region = aws_region
        # Using ISO format for timestamps - much easier to sort and filter later
        self.build_id = f"build-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Initialize all my pipeline components
        # TODO: Maybe add config injection to make this more flexible?
        self.code_analyzer = CodeAnalyzer()
        self.test_manager = TestManager()
        self.security_scanner = SecurityScanner()
        self.deployment_manager = DeploymentManager(aws_region=aws_region)
        self.ai_assistant = AIAssistant()
        
        logger.info(f"Pipeline initialized for {repo_url} on {branch}")

    def clone_repository(self) -> str:
        """Clone the repo and return local path - will implement with GitPython."""
        logger.info(f"Cloning {self.repo_url}:{self.branch}")
        # Will replace this with actual git clone logic
        # Using temp dirs for now but might want to cache repos later
        local_path = f"/tmp/repo-{self.build_id}"
        return local_path
    
    def run_pipeline(self) -> Dict[str, Any]:
        """Run the full pipeline with all stages and AI enhancements."""
        # Start with a results dictionary to collect all outputs
        results = {
            "build_id": self.build_id,
            "repository": self.repo_url,
            "branch": self.branch,
            "started_at": datetime.now().isoformat(),
            "stages": {}
        }
        
        try:
            # First grab the code
            repo_path = self.clone_repository()
            
            # STAGE 1: Static code analysis with AI enhancement
            # The AI helps identify issues that standard linters miss
            logger.info("Running code analysis")
            code_issues = self.code_analyzer.analyze(repo_path)
            ai_code_suggestions = self.ai_assistant.get_code_improvements(code_issues)
            results["stages"]["code_analysis"] = {
                "issues_found": len(code_issues),
                "ai_suggestions": ai_code_suggestions
            }
            
            # STAGE 2: Security scanning with AI risk assessment
            # AI helps prioritize vulnerabilities based on app context
            logger.info("Scanning for security issues")
            security_findings = self.security_scanner.scan(repo_path)
            ai_security_assessment = self.ai_assistant.assess_security_risks(security_findings)
            results["stages"]["security_scan"] = {
                "vulnerabilities": len(security_findings),
                "ai_risk_assessment": ai_security_assessment
            }
            
            # STAGE 3: Running tests with AI recommendations
            # AI suggests what tests we should add based on code changes
            logger.info("Running test suite")
            test_results = self.test_manager.run_tests(repo_path)
            code_changes = self.code_analyzer.get_recent_changes(repo_path)
            ai_test_suggestions = self.ai_assistant.suggest_additional_tests(code_changes, test_results)
            results["stages"]["testing"] = {
                "passed": test_results["passed"],
                "failed": test_results["failed"],
                "coverage": test_results["coverage"],
                "ai_test_suggestions": ai_test_suggestions
            }
            
            # STAGE 4: Infrastructure validation
            # Check Terraform/CloudFormation and get AI insights
            logger.info("Validating infrastructure code")
            iac_files = self.code_analyzer.find_iac_files(repo_path)
            if iac_files:
                iac_validation = self.deployment_manager.validate_infrastructure(iac_files)
                ai_iac_analysis = self.ai_assistant.analyze_infrastructure_changes(iac_files)
                results["stages"]["infrastructure_validation"] = {
                    "valid": iac_validation["valid"],
                    "errors": iac_validation["errors"],
                    "ai_analysis": ai_iac_analysis
                }
            
            # STAGE 5: Deployment with risk analysis
            # This is the coolest part - AI decides if it's safe to deploy
            if all(stage.get("passed", True) for stage in results["stages"].values()):
                logger.info("Creating deployment plan")
                deployment_plan = self.deployment_manager.create_deployment_plan(repo_path)
                ai_deployment_risks = self.ai_assistant.assess_deployment_risks(
                    deployment_plan, 
                    results["stages"]["testing"],
                    results["stages"].get("infrastructure_validation", {})
                )
                
                # Only deploy if the AI thinks it's safe (risk level ≤ 3)
                if ai_deployment_risks["risk_level"] <= 3:
                    logger.info("Deployment approved - executing")
                    deployment_result = self.deployment_manager.deploy(deployment_plan)
                    results["stages"]["deployment"] = {
                        "success": deployment_result["success"],
                        "environment": deployment_result["environment"],
                        "ai_risk_assessment": ai_deployment_risks
                    }
                else:
                    # This is where the AI really helps - prevents risky deploys
                    logger.warning(f"Deployment halted - risk too high: {ai_deployment_risks['risk_level']}/5")
                    results["stages"]["deployment"] = {
                        "success": False,
                        "halted_reason": "High risk assessment",
                        "ai_risk_assessment": ai_deployment_risks
                    }
            
            # Final AI summary with learnings and insights
            results["ai_summary"] = self.ai_assistant.generate_build_summary(results)
            
        except Exception as e:
            # Proper error handling is important for CI/CD reliability
            logger.error(f"Pipeline failed: {str(e)}")
            results["error"] = str(e)
            results["success"] = False
        else:
            results["success"] = True
        finally:
            results["completed_at"] = datetime.now().isoformat()
            
        return results


# My implementation of the AI assistant that powers the pipeline
class AIAssistant:
    """
    This is the secret sauce of my pipeline - interfaces with LLMs
    to provide smart analysis of code, security, and deployment risks.
    
    Currently using AWS Bedrock with Claude, but designed to be model-agnostic.
    """
    
    def __init__(self, model_name: str = "amazon-bedrock-claude-3-sonnet"):
        self.model_name = model_name
        self.context_window = []  # For future: maintain context across API calls
        logger.info(f"AI Assistant ready with {model_name}")
    
    def get_code_improvements(self, code_issues: List[Dict]) -> Dict:
        """Gets smarter code improvement suggestions from the LLM."""
        # No need to bother the LLM if there are no issues
        if not code_issues:
            return {"suggestions": []}
        
        prompt = self._build_code_improvement_prompt(code_issues)
        response = self._call_llm(prompt)
        
        # Parse the LLM's response into structured data
        return self._parse_code_suggestions(response)
    
    def assess_security_risks(self, security_findings: List[Dict]) -> Dict:
        """Gets the LLM to assess and prioritize security issues."""
        # Quick return for clean scans
        if not security_findings:
            return {"risk_level": 0, "analysis": "No security issues found."}
        
        prompt = self._build_security_assessment_prompt(security_findings)
        response = self._call_llm(prompt)
        
        return self._parse_security_assessment(response)
    
    def suggest_additional_tests(self, code_changes: Dict, test_results: Dict) -> Dict:
        """Uses the LLM to suggest tests based on recent code changes."""
        prompt = self._build_test_suggestion_prompt(code_changes, test_results)
        response = self._call_llm(prompt)
        
        return self._parse_test_suggestions(response)
    
    def analyze_infrastructure_changes(self, iac_files: List[str]) -> Dict:
        """Has the LLM review infrastructure code for issues and optimizations."""
        prompt = self._build_iac_analysis_prompt(iac_files)
        response = self._call_llm(prompt)
        
        return self._parse_iac_analysis(response)
    
    def assess_deployment_risks(self, deployment_plan: Dict, test_results: Dict, iac_validation: Dict) -> Dict:
        """The crown jewel - LLM assesses overall deployment risk."""
        prompt = self._build_deployment_risk_prompt(deployment_plan, test_results, iac_validation)
        response = self._call_llm(prompt)
        
        return self._parse_deployment_risks(response)
    
    def generate_build_summary(self, pipeline_results: Dict) -> Dict:
        """Has the LLM generate an executive summary of the build results."""
        prompt = self._build_summary_prompt(pipeline_results)
        response = self._call_llm(prompt)
        
        return self._parse_build_summary(response)
    
    def _call_llm(self, prompt: str) -> str:
        """Calls the LLM API - would use AWS Bedrock in production."""
        # In a real implementation, I'd connect to AWS Bedrock here
        # Would also add retry logic, error handling, etc.
        logger.info(f"Sending prompt to LLM (length: {len(prompt)})")
        
        # For demo purposes, just returning a placeholder
        # TODO: Replace with actual API call to Bedrock
        return "AI analysis complete. See structured response for details."
    
    def _build_code_improvement_prompt(self, code_issues: List[Dict]) -> str:
        """Crafts a detailed prompt for code improvement suggestions."""
        # Need to work on engineering better prompts that get more useful responses
        return f"Analyze these code issues and suggest improvements: {json.dumps(code_issues)}"
    
    # Would implement all these helper methods with proper prompt engineering
    # and response parsing logic in a complete implementation
    
    def _parse_code_suggestions(self, response: str) -> Dict:
        """Parses the LLM's response into actionable code suggestions."""
        # This is just a mock implementation
        # Would use regex or JSON parsing in the real version
        return {"suggestions": ["Implement error handling for API calls", "Add input validation"]}
    
    def _build_security_assessment_prompt(self, security_findings: List[Dict]) -> str:
        """Crafts a prompt that gets the LLM to assess security risks."""
        return f"Assess these security findings and prioritize risks: {json.dumps(security_findings)}"
    
    def _parse_security_assessment(self, response: str) -> Dict:
        """Extracts structured security assessment from LLM response."""
        # Would implement proper parsing here
        # For now, returning mock data that looks realistic
        return {
            "risk_level": 2,
            "critical_issues": 0,
            "high_issues": 1,
            "medium_issues": 3,
            "analysis": "One high-priority dependency vulnerability requires immediate attention."
        }
    
    # Would implement the remaining helper methods following the same pattern


# Quick test to make sure everything works
if __name__ == "__main__":
    # This is just for testing during development
    pipeline = AICICDPipeline(
        repo_url="https://github.com/marqeta/example-service",
        branch="main"
    )
    results = pipeline.run_pipeline()
    print(f"Pipeline run complete: {'✅ SUCCESS' if results['success'] else '❌ FAILED'}")
    print(f"AI Summary: {results.get('ai_summary', {}).get('conclusion', 'No summary available')}")
