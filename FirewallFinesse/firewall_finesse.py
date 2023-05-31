import logging
import random
import requests
import re

from rule_manager import RuleManager

class FirewallFinesse:
    def __init__(self, db_connection):
        self.rule_manager = RuleManager(db_connection)
      
    
    def generate_waf_rule(self, attack_pattern, custom_input):
        attack_patterns = self.rule_manager.load_attack_patterns_from_database()
        if attack_pattern not in attack_patterns:
            raise ValueError('Invalid attack pattern selected.')
        
        rule_template = attack_patterns[attack_pattern]
        generated_rule = rule_template.replace('<rule_template>', custom_input)
        
        return generated_rule
    
    def validate_input(self, input_value):
        if not re.match(r'^[a-zA-Z0-9_\-\.]+$', input_value):
            raise ValueError('Invalid input format. Only alphanumeric characters, underscores, dashes, and dots are allowed.')
        if re.match(r'^[\d_]+$', input_value):
            raise ValueError('Invalid input format. Alphabetic characters are required.')
        if len(input_value) < 3:
            raise ValueError('Input is too short. Minimum length should be 3 characters.')
        if re.search(r'admin|root|superuser', input_value, re.IGNORECASE):
            raise ValueError('Invalid input format. Reserved keywords are not allowed.')
    
    def generate_random_attack(self):
        attack_patterns = self.rule_manager.load_attack_patterns_from_database()
        return random.choice(list(attack_patterns.items()))
    
    def prioritize_rules(self, rules, criteria):
        prioritized_rules = sorted(rules, key=criteria)
        return prioritized_rules
    
    def fetch_external_rules(self, api_url):
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            external_rules = response.json()
            return external_rules
        except requests.exceptions.RequestException as e:
            logging.error(f'Error occurred while fetching external rules: {e}')
            return []
        except ValueError as e:
            logging.error(f'Error parsing external rule data: {e}')
            return []
    
    def analyze_rules(self, rules):
        analysis = {
            'total_rules': len(rules),
            'unique_patterns': len(set(rules)),
            'rule_lengths': [len(rule) for rule in rules],
            'most_common_patterns': self.find_most_common_patterns(rules),
        }
        return analysis
    
    def find_most_common_patterns(self, rules, num_patterns=3):
        pattern_counts = {}
        for rule in rules:
            pattern = re.search(r'<rule_template> (.+?) pattern', rule).group(1)
            if pattern in pattern_counts:
                pattern_counts[pattern] += 1
            else:
                pattern_counts[pattern] = 1
        sorted_patterns = sorted(pattern_counts, key=lambda pattern: pattern_counts[pattern], reverse=True)
        return sorted_patterns
