CREATE_INNOVATION_IDEA_RATE = """
INSERT INTO innovation_idea_rates
(innovation_idea_id, manager_id, rate) VALUES (%s, %s, %s)
RETURNING id, created_at, updated_at;
"""
