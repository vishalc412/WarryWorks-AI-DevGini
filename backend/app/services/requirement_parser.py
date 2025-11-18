"""
Requirement Parser Service
Parses and categorizes user requirements into structured data
"""
import re
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class RequirementParser:
    """Service to parse and analyze user requirements"""

    def __init__(self):
        self.feature_keywords = [
            "user", "customer", "admin", "dashboard", "report", "notification",
            "authentication", "authorization", "payment", "search", "filter",
            "export", "import", "integration", "api", "upload", "download"
        ]

        self.nfr_keywords = {
            "performance": ["fast", "performance", "speed", "latency", "response time"],
            "scalability": ["scale", "scalable", "growth", "users", "concurrent"],
            "security": ["secure", "security", "encrypt", "authentication", "authorization"],
            "availability": ["available", "uptime", "24/7", "high availability"],
            "reliability": ["reliable", "reliability", "failover", "backup"],
            "usability": ["user-friendly", "intuitive", "easy to use", "ux", "ui"]
        }

        self.tech_keywords = {
            "frontend": ["react", "angular", "vue", "next.js", "ui", "frontend"],
            "backend": ["python", "java", "node", "fastapi", "spring boot", "backend"],
            "database": ["database", "postgresql", "mysql", "mongodb", "redis"],
            "cloud": ["aws", "azure", "gcp", "cloud", "kubernetes", "docker"]
        }

    def parse(self, requirement_text: str) -> Dict[str, Any]:
        """
        Parse requirement text and extract structured information

        Args:
            requirement_text: Raw requirement text from user

        Returns:
            Structured requirement data
        """
        logger.info(f"Parsing requirement: {requirement_text[:100]}...")

        parsed_data = {
            "raw_text": requirement_text,
            "domain": self._extract_domain(requirement_text),
            "features": self._extract_features(requirement_text),
            "entities": self._extract_entities(requirement_text),
            "actions": self._extract_actions(requirement_text),
            "nfrs": self._extract_nfrs(requirement_text),
            "tech_preferences": self._extract_tech_preferences(requirement_text),
            "complexity_score": self._calculate_complexity(requirement_text),
            "categories": self._categorize_requirement(requirement_text)
        }

        logger.info(f"Parsed requirement - Domain: {parsed_data['domain']}, Features: {len(parsed_data['features'])}")
        return parsed_data

    def _extract_domain(self, text: str) -> str:
        """Extract application domain/type"""
        text_lower = text.lower()

        domain_patterns = {
            "e-commerce": ["shop", "store", "cart", "checkout", "product", "order"],
            "social_media": ["social", "post", "feed", "comment", "like", "share"],
            "healthcare": ["patient", "doctor", "appointment", "medical", "health"],
            "education": ["student", "course", "lesson", "learning", "education"],
            "finance": ["payment", "transaction", "banking", "finance", "invoice"],
            "crm": ["customer", "lead", "contact", "sales", "pipeline"],
            "analytics": ["analytics", "dashboard", "metrics", "reporting", "visualization"],
            "project_management": ["project", "task", "milestone", "team", "collaboration"]
        }

        for domain, keywords in domain_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                return domain

        return "general"

    def _extract_features(self, text: str) -> List[str]:
        """Extract potential features from text"""
        features = []
        text_lower = text.lower()

        for keyword in self.feature_keywords:
            if keyword in text_lower:
                # Extract sentences containing the keyword
                sentences = re.split(r'[.!?]', text)
                for sentence in sentences:
                    if keyword in sentence.lower():
                        features.append(sentence.strip())

        return list(set(features))[:10]  # Limit to 10 unique features

    def _extract_entities(self, text: str) -> List[str]:
        """Extract potential data entities (nouns)"""
        # Simple noun extraction using capitalized words and common entity patterns
        entities = []

        # Find capitalized words (potential entities)
        capitalized = re.findall(r'\b[A-Z][a-z]+\b', text)
        entities.extend(capitalized)

        # Common entity patterns
        entity_patterns = [
            r'\b(user|customer|admin|product|order|item|category|payment|invoice|report)\b'
        ]

        for pattern in entity_patterns:
            matches = re.findall(pattern, text.lower())
            entities.extend(matches)

        return list(set(entities))[:15]

    def _extract_actions(self, text: str) -> List[str]:
        """Extract action verbs (what the system should do)"""
        action_verbs = [
            "create", "read", "update", "delete", "manage", "view", "edit",
            "add", "remove", "search", "filter", "sort", "export", "import",
            "send", "receive", "process", "validate", "authenticate", "authorize"
        ]

        actions = []
        text_lower = text.lower()

        for verb in action_verbs:
            if verb in text_lower:
                actions.append(verb)

        return list(set(actions))

    def _extract_nfrs(self, text: str) -> Dict[str, List[str]]:
        """Extract non-functional requirements"""
        nfrs = {}
        text_lower = text.lower()

        for category, keywords in self.nfr_keywords.items():
            found = []
            for keyword in keywords:
                if keyword in text_lower:
                    found.append(keyword)
            if found:
                nfrs[category] = found

        return nfrs

    def _extract_tech_preferences(self, text: str) -> Dict[str, List[str]]:
        """Extract technology preferences"""
        tech_prefs = {}
        text_lower = text.lower()

        for category, keywords in self.tech_keywords.items():
            found = []
            for keyword in keywords:
                if keyword in text_lower:
                    found.append(keyword)
            if found:
                tech_prefs[category] = found

        return tech_prefs

    def _calculate_complexity(self, text: str) -> int:
        """Calculate complexity score (0-100)"""
        score = 0

        # Length-based complexity
        word_count = len(text.split())
        if word_count > 100:
            score += 30
        elif word_count > 50:
            score += 20
        else:
            score += 10

        # Feature complexity
        features = self._extract_features(text)
        score += min(len(features) * 5, 30)

        # Technical complexity
        tech_prefs = self._extract_tech_preferences(text)
        score += len(tech_prefs) * 10

        # NFR complexity
        nfrs = self._extract_nfrs(text)
        score += len(nfrs) * 5

        return min(score, 100)

    def _categorize_requirement(self, text: str) -> List[str]:
        """Categorize requirement type"""
        categories = []

        if any(word in text.lower() for word in ["create", "new", "build"]):
            categories.append("new_development")

        if any(word in text.lower() for word in ["improve", "enhance", "optimize"]):
            categories.append("enhancement")

        if any(word in text.lower() for word in ["fix", "bug", "issue"]):
            categories.append("bug_fix")

        if any(word in text.lower() for word in ["migrate", "upgrade", "refactor"]):
            categories.append("refactoring")

        if not categories:
            categories.append("general")

        return categories
