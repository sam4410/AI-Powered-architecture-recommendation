from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import List, Dict, Any

@CrewBase
class MultiAgentArchitectureRecommender():
    """MultiAgentArchitectureRecommender crew"""
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
   
    @agent
    def scalability_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['scalability_architect'],
            verbose=True,
            allow_delegation=False
        )
    
    @agent
    def team_structure_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['team_structure_analyst'],
            verbose=True,
            allow_delegation=False
        )
   
    @agent
    def cost_optimization_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['cost_optimization_analyst'],
            verbose=True,
            allow_delegation=False
        )
        
    @agent
    def compliance_and_security_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['compliance_and_security_expert'],
            verbose=True,
            allow_delegation=False
        )
        
    @agent
    def technology_integration_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['technology_integration_specialist'],
            verbose=True,
            allow_delegation=False
        )
   
    @agent
    def architecture_synthesis_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['architecture_synthesis_expert'],
            verbose=True,
            allow_delegation=False
        )
    
    @task
    def scalability_task(self) -> Task:
        return Task(
            config=self.tasks_config['scalability_task'],
            agent=self.scalability_architect()  # Changed from 'agents' to 'agent'
        )
    
    @task
    def team_task(self) -> Task:
        return Task(
            config=self.tasks_config['team_task'],
            agent=self.team_structure_analyst()  # Changed from 'agents' to 'agent'
        )
    
    @task
    def cost_task(self) -> Task:
        return Task(
            config=self.tasks_config['cost_task'],
            agent=self.cost_optimization_analyst()  # Changed from 'agents' to 'agent'
        )
        
    @task
    def compliance_and_security_task(self) -> Task:
        return Task(
            config=self.tasks_config['compliance_and_security_task'],
            agent=self.compliance_and_security_expert()  # Changed from 'agents' to 'agent'
        )
        
    @task
    def technology_integration_task(self) -> Task:
        return Task(
            config=self.tasks_config['technology_integration_task'],
            agent=self.technology_integration_specialist()  # Changed from 'agents' to 'agent'
        )
    
   
    @task
    def synthesis_task(self) -> Task:
        return Task(
            config=self.tasks_config['synthesis_task'],
            agent=self.architecture_synthesis_expert(),  # Changed from 'agents' to 'agent'
            context=[self.scalability_task(), self.team_task(), self.cost_task()]
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the MultiAgentArchitectureRecommender crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
