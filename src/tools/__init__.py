"""Tools = the agent's hands.

Each tool does ONE thing (SRP) and declares its own risk level. New tools
register themselves, so adding capability never means editing the planner or
the registry's logic (Open/Closed).
"""
