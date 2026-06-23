"""
Agent-Based Address Matching System
Main orchestration for Claude agent with tools
"""

import anthropic
import json
from typing import Any, Optional
from dataclasses import dataclass
from enum import Enum


class ConfidenceLevel(Enum):
    HIGH = "HIGH"      # >= 0.95
    MEDIUM = "MEDIUM"  # >= 0.80
    LOW = "LOW"        # < 0.80


@dataclass
class MatchResult:
    is_match: bool
    confidence: float
    confidence_level: ConfidenceLevel
    reasoning: str
    flags: list
    method: str
    tool_calls: list
    latency_ms: float


class AddressMatchingAgent:
    """
    Claude-based agent for intelligent address matching.
    Uses tool_use to call multiple data sources and reason about matches.
    """

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
        self.tools = self._define_tools()

    def _define_tools(self) -> list:
        """Define tools the agent can use"""
        return [
            {
                "name": "fuzzy_match_component",
                "description": "Compare two address components using fuzzy logic (Jaro-Winkler, Levenshtein). Returns similarity score 0-1.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "component1": {"type": "string", "description": "First address component"},
                        "component2": {"type": "string", "description": "Second address component"},
                        "component_type": {
                            "type": "string",
                            "enum": ["street_name", "city", "state", "street_type"],
                            "description": "Type of address component"
                        }
                    },
                    "required": ["component1", "component2", "component_type"]
                }
            },
            {
                "name": "validate_with_usps",
                "description": "Validate address against USPS database and get standardized format",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "address": {"type": "string", "description": "Full address to validate"}
                    },
                    "required": ["address"]
                }
            },
            {
                "name": "geocode_address",
                "description": "Get latitude/longitude for address and verify coordinates match",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "address": {"type": "string", "description": "Address to geocode"}
                    },
                    "required": ["address"]
                }
            },
            {
                "name": "check_tax_records",
                "description": "Look up property in county tax database for verification",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"},
                        "state": {"type": "string"},
                        "zip_code": {"type": "string"}
                    },
                    "required": ["street", "city", "state"]
                }
            },
            {
                "name": "query_knowledge_graph",
                "description": "Query knowledge graph for address variations and relationships",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "address": {"type": "string"},
                        "query_type": {
                            "type": "string",
                            "enum": ["similar_addresses", "alternate_formats", "property_info"]
                        }
                    },
                    "required": ["address", "query_type"]
                }
            },
            {
                "name": "semantic_similarity_search",
                "description": "Use embeddings to find semantically similar addresses",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "address": {"type": "string"},
                        "candidates": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Candidate addresses to compare"
                        }
                    },
                    "required": ["address", "candidates"]
                }
            }
        ]

    def match_addresses(self, user_address: str, db_address: str) -> MatchResult:
        """
        Main method: Match two addresses using agent reasoning.
        Agent iteratively calls tools and makes decision.
        """
        import time
        start_time = time.time()

        system_prompt = """You are an expert address matching agent. Your task is to determine
        if two addresses refer to the same physical location.

        STRATEGY:
        1. Start with quick fuzzy matching of components
        2. If unclear, validate both addresses with USPS
        3. Compare geocoded coordinates (geographic truth)
        4. Check property records (tax database)
        5. Query knowledge graph for known variations
        6. Use semantic embeddings as tie-breaker

        DECISION RULES:
        - If all components match perfectly: MATCH (confidence 0.99)
        - If 4/5 components match + USPS valid + coordinates match: MATCH (confidence 0.95)
        - If street/city/state match but ZIP differs: POSSIBLE MATCH (flag as concern)
        - If coordinates differ significantly: NOT A MATCH (confidence < 0.5)

        Be thorough but efficient. Provide reasoning for decision."""

        user_message = f"""Match these two addresses:

USER ADDRESS: {user_address}
DATABASE ADDRESS: {db_address}

Analyze comprehensively. Call tools as needed."""

        messages = [{"role": "user", "content": user_message}]
        tool_calls_log = []

        # Agent loop
        max_iterations = 10
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # Call Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=system_prompt,
                tools=self.tools,
                messages=messages
            )

            # Check stop reason
            if response.stop_reason == "tool_use":
                # Process tool calls
                tool_results = []

                for content_block in response.content:
                    if content_block.type == "tool_use":
                        tool_name = content_block.name
                        tool_input = content_block.input
                        tool_use_id = content_block.id

                        # Execute tool
                        result = self._execute_tool(tool_name, tool_input)
                        tool_calls_log.append({
                            "tool": tool_name,
                            "input": tool_input,
                            "output": result
                        })

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": json.dumps(result)
                        })

                # Add to conversation
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})

            else:
                # Agent finished (stop_reason == "end_turn")
                final_response = ""
                for content_block in response.content:
                    if hasattr(content_block, 'text'):
                        final_response += content_block.text

                # Parse decision
                result = self._parse_decision(final_response, tool_calls_log)
                result.latency_ms = (time.time() - start_time) * 1000

                return result

        # Max iterations reached
        return MatchResult(
            is_match=False,
            confidence=0.0,
            confidence_level=ConfidenceLevel.LOW,
            reasoning="Agent max iterations exceeded",
            flags=["TIMEOUT"],
            method="agent_timeout",
            tool_calls=tool_calls_log,
            latency_ms=(time.time() - start_time) * 1000
        )

    def _execute_tool(self, tool_name: str, tool_input: dict) -> Any:
        """Execute a tool and return results"""
        from tools.fuzzy_matcher import FuzzyMatcher
        from tools.validators import USPSValidator, TaxRecordValidator, GeocodeValidator

        if tool_name == "fuzzy_match_component":
            comp1 = tool_input["component1"]
            comp2 = tool_input["component2"]
            comp_type = tool_input["component_type"]

            if comp_type == "street_name":
                score = FuzzyMatcher.jaro_winkler_similarity(comp1, comp2)
            elif comp_type == "city":
                score = FuzzyMatcher.jaro_winkler_similarity(comp1, comp2)
                if score < 0.8:
                    score = max(score, FuzzyMatcher.phonetic_similarity(comp1, comp2))
            else:
                score = 1.0 if comp1.upper() == comp2.upper() else 0.0

            return {
                "component_type": comp_type,
                "score": round(score, 3),
                "match": score >= 0.85,
                "comp1": comp1,
                "comp2": comp2
            }

        elif tool_name == "validate_with_usps":
            validator = USPSValidator()
            return validator.validate(tool_input["address"])

        elif tool_name == "geocode_address":
            validator = GeocodeValidator()
            return validator.geocode(tool_input["address"])

        elif tool_name == "check_tax_records":
            validator = TaxRecordValidator()
            return validator.lookup(
                tool_input.get("street"),
                tool_input.get("city"),
                tool_input.get("state"),
                tool_input.get("zip_code", "")
            )

        elif tool_name == "query_knowledge_graph":
            from tools.knowledge_graph import KnowledgeGraph
            kg = KnowledgeGraph()
            query_type = tool_input["query_type"]

            if query_type == "similar_addresses":
                return kg.find_similar(tool_input["address"])
            elif query_type == "alternate_formats":
                return kg.find_alternates(tool_input["address"])
            else:
                return kg.get_property_info(tool_input["address"])

        elif tool_name == "semantic_similarity_search":
            from tools.embeddings import EmbeddingMatcher
            matcher = EmbeddingMatcher()
            return matcher.find_similar(
                tool_input["address"],
                tool_input.get("candidates", [])
            )

        return {"error": f"Unknown tool: {tool_name}"}

    def _parse_decision(self, response_text: str, tool_calls: list) -> MatchResult:
        """Parse agent's decision from response"""
        import re

        # Extract match decision
        is_match = "match" in response_text.lower() and "no match" not in response_text.lower()

        # Extract confidence
        confidence_patterns = [
            r'confidence[:\s]+(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*(?:confidence|certain)',
            r'confidence[:\s]+(very\s+high|high|medium|low)'
        ]

        confidence = 0.75
        for pattern in confidence_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                val = match.group(1)
                if val.replace('.', '', 1).isdigit():
                    confidence = float(val)
                    if confidence > 1:
                        confidence /= 100
                break

        # Determine confidence level
        if confidence >= 0.95:
            confidence_level = ConfidenceLevel.HIGH
        elif confidence >= 0.80:
            confidence_level = ConfidenceLevel.MEDIUM
        else:
            confidence_level = ConfidenceLevel.LOW

        # Extract flags
        flag_patterns = [r'flag[:\s]+([^\.]+)', r'concern[:\s]+([^\.]+)']
        flags = []
        for pattern in flag_patterns:
            matches = re.findall(pattern, response_text, re.IGNORECASE)
            flags.extend([m.strip() for m in matches])

        return MatchResult(
            is_match=is_match,
            confidence=min(confidence, 1.0),
            confidence_level=confidence_level,
            reasoning=response_text[:1000],
            flags=flags,
            method="agent_reasoning",
            tool_calls=tool_calls,
            latency_ms=0
        )
