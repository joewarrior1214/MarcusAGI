#!/usr/bin/env python3
"""
Marcus's Simple Virtual Body - Grid World
Start here! This is the minimal viable embodiment.
"""

import numpy as np
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any
from MarcusAGI.memory_system import MarcusMemorySystem

class MarcusGridWorld:
    """A simple 2D grid world for Marcus to explore and learn physics"""
    
    def __init__(self, size: int = 10):
        self.size = size
        self.grid = np.zeros((size, size))
        self.marcus_pos = [size//2, size//2]
        self.objects = {}
        self.experiences = []
        
        # Marcus's body state
        self.holding = None
        self.energy = 100
        self.facing = 'north'  # north, south, east, west
        
        # Sensory data
        self.vision_range = 3
        self.touch_sensor = False
        
        # Initialize some objects
        self._place_objects()
        
    def _place_objects(self):
        """Place some objects for Marcus to interact with"""
        # Place a ball
        self.objects['ball_1'] = {
            'type': 'ball',
            'pos': [2, 2],
            'weight': 1,
            'color': 'red',
            'movable': True
        }
        
        # Place a heavy block
        self.objects['block_1'] = {
            'type': 'block',
            'pos': [7, 7],
            'weight': 5,
            'color': 'blue',
            'movable': True
        }
        
        # Place a wall (immovable)
        self.objects['wall_1'] = {
            'type': 'wall',
            'pos': [5, 5],
            'weight': 999,
            'color': 'gray',
            'movable': False
        }
        
        self._update_grid()
    
    def _update_grid(self):
        """Update grid visualization"""
        self.grid = np.zeros((self.size, self.size))
        
        # Place objects
        for obj_id, obj in self.objects.items():
            x, y = obj['pos']
            self.grid[x, y] = 2 if obj['movable'] else 3
        
        # Place Marcus
        self.grid[self.marcus_pos[0], self.marcus_pos[1]] = 1
    
    def move(self, direction: str) -> Dict[str, Any]:
        """Move Marcus in a direction"""
        old_pos = self.marcus_pos.copy()
        
        # Calculate new position
        moves = {
            'north': [-1, 0],
            'south': [1, 0],
            'east': [0, 1],
            'west': [0, -1]
        }
        
        if direction not in moves:
            return {'success': False, 'reason': 'Invalid direction'}
        
        new_pos = [
            self.marcus_pos[0] + moves[direction][0],
            self.marcus_pos[1] + moves[direction][1]
        ]
        
        # Check boundaries
        if not (0 <= new_pos[0] < self.size and 0 <= new_pos[1] < self.size):
            # Learning experience: boundaries exist!
            experience = {
                'action': 'move',
                'result': 'hit_boundary',
                'learning': 'World has edges I cannot pass',
                'timestamp': datetime.now().isoformat()
            }
            self.experiences.append(experience)
            return {'success': False, 'reason': 'Hit boundary', 'learning': experience}
        
        # Check for obstacles
        for obj_id, obj in self.objects.items():
            if obj['pos'] == new_pos:
                if not obj['movable']:
                    # Learning experience: some things don't move
                    experience = {
                        'action': 'move_into_wall',
                        'result': 'blocked',
                        'learning': f"Some objects ({obj['type']}) cannot be moved through",
                        'timestamp': datetime.now().isoformat()
                    }
                    self.experiences.append(experience)
                    return {'success': False, 'reason': 'Blocked by wall', 'learning': experience}
        
        # Successful move
        self.marcus_pos = new_pos
        self.facing = direction
        self.energy -= 1
        self._update_grid()
        
        # Learning experience: movement costs energy
        if len(self.experiences) < 5:  # Only record early on
            experience = {
                'action': 'move',
                'result': 'success',
                'learning': 'Moving uses energy',
                'energy_before': self.energy + 1,
                'energy_after': self.energy,
                'timestamp': datetime.now().isoformat()
            }
            self.experiences.append(experience)
        
        return {'success': True, 'new_pos': new_pos, 'energy': self.energy}
    
    def grab(self) -> Dict[str, Any]:
        """Try to grab object in front of Marcus"""
        # Calculate position in front
        front_offsets = {
            'north': [-1, 0],
            'south': [1, 0],
            'east': [0, 1],
            'west': [0, -1]
        }
        
        front_pos = [
            self.marcus_pos[0] + front_offsets[self.facing][0],
            self.marcus_pos[1] + front_offsets[self.facing][1]
        ]
        
        # Check if already holding something
        if self.holding:
            return {'success': False, 'reason': 'Already holding something'}
        
        # Look for object at front position
        for obj_id, obj in self.objects.items():
            if obj['pos'] == front_pos:
                if obj['weight'] > 10:
                    # Learning: some things are too heavy
                    experience = {
                        'action': 'grab',
                        'object': obj['type'],
                        'weight': obj['weight'],
                        'result': 'too_heavy',
                        'learning': f"Objects with weight > 10 are too heavy to lift",
                        'timestamp': datetime.now().isoformat()
                    }
                    self.experiences.append(experience)
                    return {'success': False, 'reason': 'Too heavy', 'learning': experience}
                
                # Success! Pick it up
                self.holding = obj_id
                obj['pos'] = None  # Object is now held
                self._update_grid()
                
                # Learning: different objects have different weights
                experience = {
                    'action': 'grab',
                    'object': obj['type'],
                    'weight': obj['weight'],
                    'color': obj['color'],
                    'result': 'success',
                    'learning': f"I can lift {obj['type']} (weight: {obj['weight']})",
                    'timestamp': datetime.now().isoformat()
                }
                self.experiences.append(experience)
                
                return {'success': True, 'holding': obj_id, 'object_data': obj, 'learning': experience}
        
        return {'success': False, 'reason': 'Nothing to grab'}
    
    def drop(self) -> Dict[str, Any]:
        """Drop held object"""
        if not self.holding:
            return {'success': False, 'reason': 'Not holding anything'}
        
        # Calculate drop position (in front)
        front_offsets = {
            'north': [-1, 0],
            'south': [1, 0],
            'east': [0, 1],
            'west': [0, -1]
        }
        
        drop_pos = [
            self.marcus_pos[0] + front_offsets[self.facing][0],
            self.marcus_pos[1] + front_offsets[self.facing][1]
        ]
        
        # Check if position is free
        for obj_id, obj in self.objects.items():
            if obj['pos'] == drop_pos:
                return {'success': False, 'reason': 'Position occupied'}
        
        # Drop the object
        self.objects[self.holding]['pos'] = drop_pos
        dropped_obj = self.objects[self.holding]
        self.holding = None
        self._update_grid()
        
        # Learning: objects fall when released
        experience = {
            'action': 'drop',
            'object': dropped_obj['type'],
            'result': 'object_fell',
            'learning': 'Objects fall when I let go (gravity exists!)',
            'timestamp': datetime.now().isoformat()
        }
        self.experiences.append(experience)
        
        return {'success': True, 'dropped_at': drop_pos, 'learning': experience}
    
    def look(self) -> Dict[str, Any]:
        """Get visual information about surroundings"""
        visible_objects = []
        
        # Simple vision: can see in a square around Marcus
        for dx in range(-self.vision_range, self.vision_range + 1):
            for dy in range(-self.vision_range, self.vision_range + 1):
                check_pos = [self.marcus_pos[0] + dx, self.marcus_pos[1] + dy]
                
                # Check bounds
                if 0 <= check_pos[0] < self.size and 0 <= check_pos[1] < self.size:
                    # Check for objects
                    for obj_id, obj in self.objects.items():
                        if obj['pos'] == check_pos:
                            distance = abs(dx) + abs(dy)  # Manhattan distance
                            visible_objects.append({
                                'object': obj['type'],
                                'color': obj['color'],
                                'distance': distance,
                                'direction': self._get_direction(dx, dy),
                                'position': check_pos
                            })
        
        # Learning: I can see objects around me
        if len(self.experiences) < 10:
            experience = {
                'action': 'look',
                'result': f'saw {len(visible_objects)} objects',
                'learning': 'I can see objects within 3 spaces',
                'timestamp': datetime.now().isoformat()
            }
            self.experiences.append(experience)
        
        return {
            'visible_objects': visible_objects,
            'facing': self.facing,
            'vision_range': self.vision_range
        }
    
    def _get_direction(self, dx: int, dy: int) -> str:
        """Convert position difference to direction"""
        if dx < 0:
            return 'north'
        elif dx > 0:
            return 'south'
        elif dy < 0:
            return 'west'
        elif dy > 0:
            return 'east'
        else:
            return 'here'
    
    def touch(self) -> Dict[str, Any]:
        """Feel what's directly in front"""
        front_offsets = {
            'north': [-1, 0],
            'south': [1, 0],
            'east': [0, 1],
            'west': [0, -1]
        }
        
        front_pos = [
            self.marcus_pos[0] + front_offsets[self.facing][0],
            self.marcus_pos[1] + front_offsets[self.facing][1]
        ]
        
        # Check boundaries
        if not (0 <= front_pos[0] < self.size and 0 <= front_pos[1] < self.size):
            return {'feeling': 'boundary', 'learning': 'World edges feel solid'}
        
        # Check for objects
        for obj_id, obj in self.objects.items():
            if obj['pos'] == front_pos:
                texture = {
                    'ball': 'smooth',
                    'block': 'rough',
                    'wall': 'hard'
                }.get(obj['type'], 'unknown')
                
                # Learning through touch
                experience = {
                    'action': 'touch',
                    'object': obj['type'],
                    'feeling': texture,
                    'weight_estimate': 'heavy' if obj['weight'] > 3 else 'light',
                    'learning': f"{obj['type']} feels {texture}",
                    'timestamp': datetime.now().isoformat()
                }
                self.experiences.append(experience)
                
                return {
                    'object': obj['type'],
                    'texture': texture,
                    'weight_feel': 'heavy' if obj['weight'] > 3 else 'light',
                    'learning': experience
                }
        
        return {'feeling': 'empty_space', 'learning': 'Air feels like nothing'}
    
    def display(self):
        """Show Marcus's current world state - simplified version"""
        print(f"\n🌍 Marcus: Position [{self.marcus_pos[0]}, {self.marcus_pos[1]}] | Energy: {self.energy} | Holding: {self.holding or 'nothing'}")
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Summarize what Marcus has learned"""
        learnings = {}
        
        for exp in self.experiences:
            category = exp.get('action', 'unknown')
            if category not in learnings:
                learnings[category] = []
            learnings[category].append(exp.get('learning', 'unknown'))
        
        return {
            'total_experiences': len(self.experiences),
            'categories_explored': list(learnings.keys()),
            'key_learnings': learnings,
            'unique_discoveries': len(set(exp.get('learning') for exp in self.experiences))
        }
    
    def save_experiences(self, filename: str = "marcus_body_experiences.json"):
        """Save Marcus's physical experiences"""
        data = {
            'world_size': self.size,
            'total_experiences': len(self.experiences),
            'experiences': self.experiences,
            'learning_summary': self.get_learning_summary()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Saved {len(self.experiences)} physical experiences")


# Integration with Marcus's learning system
class EmbodiedLearning:
    """Connect physical experiences to concept learning"""
    
    def __init__(self, world: MarcusGridWorld):
        self.world = world
        self.memory_system = MarcusMemorySystem("marcus_embodied.db")
        self.concept_mappings = {}  # Add this missing line!
    
    def explore_and_learn(self, num_actions: int = 20):
        """Let Marcus explore and form concepts"""
        print("\n🎮 Marcus begins exploring his world...")
        
        for i in range(num_actions):
            # Decide what to do (simple random for now)
            import random
            action = random.choice(['move', 'grab', 'drop', 'look', 'touch'])
            
            if action == 'move':
                direction = random.choice(['north', 'south', 'east', 'west'])
                result = self.world.move(direction)
                if result.get('learning'):
                    # Pass the correct format with action
                    self._form_concept({
                        'learning': result['learning'],
                        'action': action
                    })
            
            elif action == 'grab':
                result = self.world.grab()
                if result.get('learning'):
                    self._form_concept({
                        'learning': result['learning'],
                        'action': action
                    })
            
            elif action == 'drop':
                result = self.world.drop()
                if result.get('learning'):
                    self._form_concept({
                        'learning': result['learning'],
                        'action': action
                    })
            
            elif action == 'look':
                result = self.world.look()
                if result['visible_objects']:
                    concept = f"I can see {len(result['visible_objects'])} objects"
                    self._form_concept({
                        'learning': concept,
                        'action': action
                    })
            
            elif action == 'touch':
                result = self.world.touch()
                if result.get('learning'):
                    self._form_concept({
                        'learning': result['learning'],
                        'action': action
                    })
            
            # Show world state occasionally
            if i % 10 == 0:
                self.world.display()
        
        return self.world.get_learning_summary()
    
    def _form_concept(self, learning_experience):
        """Convert physical experience into knowledge!"""
        
        # Extract the learning content properly
        if isinstance(learning_experience, dict):
            if 'learning' in learning_experience:
                if isinstance(learning_experience['learning'], dict):
                    # Handle nested learning object
                    concept_content = learning_experience['learning'].get('learning', str(learning_experience['learning']))
                else:
                    concept_content = str(learning_experience['learning'])
                concept_key = learning_experience.get('action', 'exploration')
            else:
                concept_content = str(learning_experience)
                concept_key = 'general'
        else:
            concept_content = str(learning_experience)
            concept_key = 'exploration'
        
        # Store in concept mappings
        if concept_key not in self.concept_mappings:
            self.concept_mappings[concept_key] = []
        
        if concept_content not in self.concept_mappings[concept_key]:
            self.concept_mappings[concept_key].append(concept_content)
            # Remove the verbose print, just show summary later
            # print(f"💡 Concept: {concept_content} (confidence: 0.2)")
            
            try:
                # Set logging level to WARNING to reduce INFO messages
                import logging
                logging.getLogger('MarcusAGI.memory_system').setLevel(logging.WARNING)
                logging.getLogger('memory_system').setLevel(logging.WARNING)
                
                from MarcusAGI.memory_system import Concept
                concept = Concept(
                    id=f"physics_{concept_key}_{len(self.concept_mappings[concept_key])}",
                    content=concept_content,
                    subject="physics",
                    grade_level="kindergarten",
                    emotional_context="discovered"
                )
                self.memory_system.learn_concept(concept)
            except Exception:
                pass  # Silent fail