import random
import math
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from collections import Counter

class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env, learning=False, epsilon=1.0, alpha=0.5):
        super(LearningAgent, self).__init__(env)     # Set the agent in the evironment 
        self.planner = RoutePlanner(self.env, self)  # Create a route planner
        self.valid_actions = self.env.valid_actions  # The set of valid actions

        # Set parameters of the learning agent
        self.learning = learning # Whether the agent is expected to learn
        self.Q = dict()          # Create a Q-table which will be a dictionary of tuples
        self.epsilon = epsilon   # Random exploration factor
        self.alpha = alpha       # Learning factor

        ###########
        ## TO DO ##
        ###########
        # Set any additional class parameters as needed

    def reset(self, destination=None, testing=False):
        """ The reset function is called at the beginning of each trial.
            'testing' is set to True if testing trials are being used
            once training trials have completed. """

        # Select the destination as the new location to route to
        self.planner.route_to(destination)
        
        ########### 
        ## TO DO ##
        ###########
        # Update epsilon using a decay function of your choice
        # Update additional class parameters as needed
        # If 'testing' is True, set epsilon and alpha to 0
        if self.epsilon > 0:
            self.epsilon -= 0.05
        # else:
        #     self.epsilon = 0
        if testing == True:
            self.alpha = 0
            self.epsilon = 0
        return None

    def build_state(self):
        """ The build_state function is called when agent requests data from  
            environment. The next waypoint, intersection inputs, and deadline 
            are all features available to the agent. """

        # Collect data about the environment
        waypoint = self.planner.next_waypoint() # The next waypoint 
        inputs = self.env.sense(self)           # Visual input - intersection light and traffic
        deadline = self.env.get_deadline(self)  # Remaining deadline

        ########### 
        ## TO DO ##
        ###########
        
        # NOTE : Do not engineer features outside inputs available.
        # Because the aim is to teach Reinforcement Learning, we have placed 
        # constraints in order for you to learn how to adjust epsilon and alpha, and thus learn about the balance between exploration and exploitation.
        # With hand-engineered features, learning process is entirely negated.
        
        # Set 'state' as a tuple of relevant data for the agent   
        # Commenting out or removing variables from 'state' should give sim_no learning     
        state = (inputs, waypoint, deadline)

        return state
        print state

    def get_maxQ(self, state):
        """ The get_max_Q function is called when the agent is asked to find
            maximum Q-value of actions based on the 'state' of smartcab. """

        ########### 
        ## TO DO ##
        ###########
        # Calculate the maximum Q-value of all actions for a given state
        for action in [None, forward, left, right]:
            maxQ = max(self.Q[state][action])

        return maxQ 

    def createQ(self, state):
        # The createQ function is called when a state is generated by agent.

        ########### 
        ## TO DO ##
        ###########
        # When learning, check if the 'state' is not in the Q-table
        # If it is not, create a new dictionary for that state
        # Then, for each action available, set the initial Q-value to 0.0
        
        # if self.learning == True:
        #     if state not in self.Q.keys():
        #         self.Q[state] = dict()
        #         for action in [None, forward, left, right]:
        #             self.Q[state][action] = 0.0

        return

    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()
        action = random.choice(self.valid_actions)

        ########### 
        ## TO DO ##
        ###########
        # When not learning, choose a random action
        # When learning, choose a random action with 'epsilon' probability
        # # Otherwise, choose an action with the highest Q-value for the current state
        # # Be sure that when choosing an action with highest Q-value that you randomly select between actions that "tie".
        
        # # Returns purely random action from list during no learning
        # if self.learning == False:
        #     return action
        
        # # Creates random integer to compare to epsilon
        # else:
        #     learning_random_val = random.randint(1, 100)
        #     # If below threshold (probability), selects random action
        #     if self.epsilon * 100 <= learning_random_val:
        #         return action
            
        #     # Otherwise the best Q action from state is selected
        #     else:
        #         # Creates tuple of highest key and value pair
        #         statemaxtuple = max(zip(self.Q[state].values(), self.Q[state].keys()))
        #         statekey, stateval = statemaxtuple[1], statemaxtuple[0]
        #         # Uses a Counter to check if a tie exists
        #         if Counter(self.Q[state].values())[stateval] > 1:
        #             statetie = [k for k, v in self.Q[state].iteritems() if v == stateval]
        #             return random.choice(statetie)
        #         else:
        #             return statemaxtuple[0]

    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives a reward. This function does not consider future rewards 
            when conducting learning. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, implement the value iteration update rule
        #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')

        return

    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        state = self.build_state()          # Get current state
        self.createQ(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)  # Choose an action
        reward = self.env.act(self, action) # Receive a reward
        self.learn(state, action, reward)   # Q-learn

        return
        
def run():
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    #   grid_size   - discrete number of intersections (columns, rows), default is (8, 6)
    env = Environment(verbose=False)
    
    ##############
    # Create the driving agent
    # Flags:
    #   learning   - set to True to force the driving agent to use Q-learning
    #    * epsilon - continuous value for the exploration factor, default is 1
    #    * alpha   - continuous value for the learning rate, default is 0.5
    agent = env.create_agent(LearningAgent, learning=True)
    
    ##############
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent, enforce_deadline=True)

    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    sim = Simulator(env, update_delay=0.01, display=True, log_metrics=True)
    # print sim.trial
    
    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05 
    #   n_test     - discrete number of testing trials to perform, default is 0
    sim.run(n_test=10)
    print agent.Q
    print agent.choose_action()
 
if __name__ == '__main__':
    run()