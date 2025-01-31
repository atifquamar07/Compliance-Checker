# app/services/text_analyzer.py
from groq import Groq
from typing import List, Dict
import json
import re
from app.config import settings
from termcolor import colored

class TextAnalyzer:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"

    async def analyze_compliance(self, webpage_content: Dict[str, str], policy_content: Dict[str, str]) -> List[Dict]:
        """
        This method performs a two-step analysis:
        1. First, it processes the policy document to understand the compliance rules
        2. Then, it checks the webpage content against these extracted rules
        """
        try:
            # Step 1: Extract rules from policy document
            rules_prompt = self._create_rules_extraction_prompt(policy_content['clean_text'])
            rules_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a compliance expert specializing in regulatory and policy analysis. Your task is to meticulously extract and list all compliance rules, requirements, and obligations from policy documents. Ensure clarity, precision, and completeness in your extraction, maintaining the original intent and legal accuracy of the document. Focus on regulatory obligations, procedural mandates, and key compliance measures, presenting them in a structured and easily understandable format. If necessary, categorize the extracted requirements based on themes such as governance, risk management, reporting, marketing and operational controls."
                    },
                    {
                        "role": "user",
                        "content": rules_prompt
                    }
                ],
                model=self.model,
                temperature=0.1
            )
            
            extracted_rules = rules_completion.choices[0].message.content
            
            # Step 2: Analyze webpage against extracted rules
            analysis_prompt = self._create_analysis_prompt(
                webpage_content['clean_text'],
                extracted_rules
            )
            
            analysis_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a compliance checker specializing in identifying policy and regulatory violations. Your task is to analyze webpage content against a set of provided rules and detect any non-compliance issues. Ensure accuracy, consistency, and relevance in your findings. Return the identified violations in a structured JSON format, including details such as the violated rule, the specific content triggering the violation, and a brief explanation. If applicable, categorize the violations based on severity or type (e.g., legal, security, accessibility, data privacy)."
                    },
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ],
                model=self.model,
                temperature=0.1
            )
            
            violations = analysis_completion.choices[0].message.content
            parsed_violations = self._parse_violations(analysis_completion.choices[0].message.content)
            
            return parsed_violations

        except Exception as e:
            return [{
                'type': 'analysis_error',
                'description': f'Error during analysis: {str(e)}',
                'context': 'System error during compliance check',
                'severity': 'high',
                'suggestion': 'Please try again or contact support'
            }]


    def _parse_violations(self, response: str) -> List[Dict]:
        """
        Extracts and parses JSON content from the LLM's response using regex.
        
        This function looks for JSON content within the response text, even if it's surrounded
        by other explanatory text. It focuses on finding content within curly braces and
        parsing it as JSON.
        
        Args:
            response: The raw response string from the LLM
            
        Returns:
            List of violation dictionaries extracted from the JSON content
        """
        try:
            # This regex pattern looks for content between outermost curly braces,
            # including nested braces. The (?s) flag allows . to match newlines
            json_pattern = r'(?s)\{.*\}'
            json_match = re.search(json_pattern, response)
            
            if json_match:
                # Extract the matched JSON string
                json_str = json_match.group(0)
                
                # Parse the extracted JSON
                data = json.loads(json_str)
                
                # If we have a violations key, return its contents
                if isinstance(data, dict) and 'violations' in data:
                    return data['violations']
                
                # If the JSON is already a list, return it directly
                if isinstance(data, list):
                    return data
            
            # If no valid JSON was found or parsed, return a parsing error
            return [{
                'type': 'parsing_error',
                'description': 'Could not find valid JSON in the response',
                'context': response[:100] + '...' if len(response) > 100 else response,
                'severity': 'high',
                'suggestion': 'Check LLM output formatting'
            }]
                
        except json.JSONDecodeError as e:
            # Handle JSON parsing errors specifically
            return [{
                'type': 'json_parsing_error',
                'description': f'Failed to parse JSON: {str(e)}',
                'context': response[:100] + '...' if len(response) > 100 else response,
                'severity': 'high',
                'suggestion': 'Verify JSON structure in LLM response'
            }]
        except Exception as e:
            # Handle any other unexpected errors
            return [{
                'type': 'unexpected_error',
                'description': f'Unexpected error during parsing: {str(e)}',
                'context': response[:100] + '...' if len(response) > 100 else response,
                'severity': 'high',
                'suggestion': 'Check system logs for details'
            }]
    
        
    def _create_rules_extraction_prompt(self, policy_text: str) -> str:
        """
        Creates a prompt to analyze the compliance policy document and extract clear, actionable rules.
        
        This method structures the prompt to help the LLM focus on specific aspects of compliance,
        ensuring we get well-organized, usable rules for our analysis.
        """
        return f"""
        Please analyze this compliance policy document and extract all marketing and compliance rules in detail:

        POLICY DOCUMENT:
        {policy_text}

        Focus on extracting explicit and implicit rules within these specific categories:

        1. **Required Terminology:**
        - Specific terms that must be used in marketing materials
        - Correct ways to describe services, products, or policies
        - Approved industry-standard terminology
        - Contextual usage guidelines (e.g., required tone or phrasing)

        2. **Prohibited Language:**
        - Terms, phrases, or claims that cannot be used
        - Misleading, exaggerated, or legally restricted language
        - Comparative statements that may violate fairness standards
        - Unsubstantiated claims or guarantees

        3. **Mandatory Disclosures:**
        - Required disclaimers for legal, financial, or regulatory purposes
        - Necessary legal text that must appear in communications
        - Rules regarding placement, font size, or prominence of disclosures
        - Language that must accompany specific claims or promotions

        4. **Marketing Guidelines:**
        - Restrictions on promotional content (e.g., no false urgency, hidden conditions)
        - Accuracy requirements (e.g., factual representation of products/services)
        - Specific marketing limitations (e.g., rules for endorsements, user testimonials)
        - Ethical considerations in marketing, including fair representation
        - Requirements for digital advertising, email marketing, and social media

        5. **Compliance Requirements:**
        - Regulatory obligations applicable to marketing and advertising
        - Specific compliance standards that must be followed
        - Documentation, record-keeping, and audit requirements
        - Rules governing customer data usage, consent, and privacy laws (e.g., GDPR, CCPA)
        - Industry-specific compliance mandates (e.g., financial services, healthcare)

        6. **Enforcement and Consequences:**
        - Potential penalties for non-compliance (e.g., fines, legal action)
        - Internal review processes and approval requirements before publication
        - Reporting mechanisms for compliance violations
        - Corrective actions or remediation procedures

        **Response Format:**
        - Provide a structured list of rules under each category.
        - Each rule should include:
            - **The specific requirement**
            - **Why it’s important (legal, ethical, reputational risks)**
            - **Examples of compliance vs. non-compliance, if available**
        - If applicable, highlight any ambiguities or areas where clarification may be needed.

        The output should be well-organized and formatted for easy compliance checking.
        """

    def _create_analysis_prompt(self, webpage_text: str, extracted_rules: str) -> str:
        """
        Creates a prompt to analyze webpage content against the extracted compliance rules.
        
        This method carefully structures the comparison between the webpage content
        and the previously extracted rules to ensure thorough compliance checking.
        """
        return f"""
        Compare this webpage content against the following compliance rules.
        Identify any violations accurately and comprehensively.

        EXTRACTED COMPLIANCE RULES:
        {extracted_rules}

        WEBPAGE CONTENT TO ANALYZE:
        {webpage_text}

        For each violation found, provide:
        1. Specific rule being violated
        2. Exact content that violates the rule
        3. Why it's a violation
        4. How to fix it

        Return your analysis in this JSON format:
        {{
            "violations": [
                {{
                    "type": "Type of violation (e.g., terminology, disclosure, marketing)",
                    "description": "A very detailed clear explanation of how content violates the rule. The detailed explanation should include the legal, ethical, or compliance implications of the violation. The description should be above 500 tokens.
                    "context": "The specific text or content that violates the rule",
                    "severity": "high/medium/low based on compliance impact",
                    "suggestion": "A deatiled Specific recommendation to achieve compliance"
                }}
            ]
        }}

        If no violations are found, return an empty violations array.
        Focus on accuracy and providing actionable insights for fixing any violations.
        """