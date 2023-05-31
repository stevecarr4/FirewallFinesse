import psycopg2

class RuleManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def load_attack_patterns_from_database(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT attack_pattern, rule_template FROM attack_patterns;")
        rows = cursor.fetchall()
        attack_patterns = {}
        for row in rows:
            attack_pattern, rule_template = row
            attack_patterns[attack_pattern] = rule_template
        return attack_patterns
    
    def add_attack_pattern_to_database(self, attack_pattern, rule_template):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO attack_patterns (attack_pattern, rule_template) VALUES (%s, %s);", (attack_pattern, rule_template))
        self.db_connection.commit()
    
    def remove_attack_pattern_from_database(self, attack_pattern):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM attack_patterns WHERE attack_pattern = %s;", (attack_pattern,))
        self.db_connection.commit()
    
    def update_attack_pattern_in_database(self, attack_pattern, new_rule_template):
        cursor = self.db_connection.cursor()
        cursor.execute("UPDATE attack_patterns SET rule_template = %s WHERE attack_pattern = %s;", (new_rule_template, attack_pattern))
        self.db_connection.commit()
