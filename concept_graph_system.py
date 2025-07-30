#!/usr/bin/env python3
"""
Marcus Concept Graph System - Feature #2
Builds a visual semantic network of Marcus's learned concepts
Shows how ideas connect in Marcus's developing mind
"""

import networkx as nx
import matplotlib.pyplot as plt
import json
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass
import math
from collections import defaultdict
from marcus_memory_system import MarcusMemorySystem, Concept

@dataclass
class ConceptConnection:
    """Represents a connection between two concepts"""
    concept1_id: str
    concept2_id: str
    connection_type: str  # "similarity", "cause_effect", "category", "emotional", "temporal"
    strength: float  # 0.0 to 1.0
    discovered_through: str  # "learning_session", "reflection", "mr_rogers_episode"
    
class MarcusConceptGraph:
    """Manages Marcus's semantic concept network"""
    
    def __init__(self, memory_system: MarcusMemorySystem):
        self.memory_system = memory_system
        self.graph = nx.Graph()
        self.concept_categories = {
            'emotions': ['angry', 'happy', 'sad', 'scared', 'excited', 'proud', 'curious'],
            'social_skills': ['friendship', 'kindness', 'sharing', 'empathy', 'helping'],  
            'moral_concepts': ['right', 'wrong', 'fairness', 'honesty', 'respect'],
            'self_concept': ['special', 'unique', 'growth', 'mistakes', 'learning'],
            'academic': ['counting', 'letters', 'colors', 'shapes', 'reading'],
            'life_skills': ['safety', 'routines', 'responsibility', 'independence']
        }
        self.connection_patterns = self._initialize_connection_patterns()
        
    def _initialize_connection_patterns(self) -> Dict[str, List[Tuple[str, str, float]]]:
        """Define patterns for automatic concept linking"""
        return {
            'emotional_similarity': [
                ('happy', 'excited', 0.7),
                ('sad', 'scared', 0.6),
                ('angry', 'frustrated', 0.8),
                ('proud', 'confident', 0.7)
            ],
            'moral_causality': [
                ('kindness', 'friendship', 0.9),
                ('sharing', 'friendship', 0.8),
                ('honesty', 'trust', 0.9),
                ('helping', 'kindness', 0.8),
                ('empathy', 'kindness', 0.9)
            ],
            'developmental_sequence': [
                ('counting_1to10', 'counting_1to20', 0.9),
                ('colors_primary', 'colors_secondary', 0.8),
                ('feelings_basic', 'feelings_complex', 0.7)
            ],
            'mr_rogers_themes': [
                ('special', 'unique', 0.9),
                ('mistakes', 'learning', 0.8),
                ('feelings', 'acceptance', 0.8),
                ('different', 'special', 0.7)
            ]
        }
    
    def add_concept_to_graph(self, concept: Concept) -> bool:
        """Add a concept to the semantic graph"""
        try:
            # Add concept as node
            self.graph.add_node(
                concept.id,
                content=concept.content,
                subject=concept.subject,
                grade_level=concept.grade_level,
                emotional_context=concept.emotional_context,
                category=self._categorize_concept(concept)
            )
            
            # Find and create connections
            self._discover_connections(concept)
            
            return True
        except Exception as e:
            print(f"Error adding concept to graph: {e}")
            return False
    
    def _categorize_concept(self, concept: Concept) -> str:
        """Categorize a concept based on content and subject"""
        content_lower = concept.content.lower()
        
        for category, keywords in self.concept_categories.items():
            for keyword in keywords:
                if keyword in content_lower or keyword in concept.id.lower():
                    return category
        
        # Subject-based categorization
        subject_map = {
            'social_emotional': 'social_skills',
            'mathematics': 'academic',
            'language_arts': 'academic',
            'art': 'academic',
            'moral_education': 'moral_concepts',
            'self_concept': 'self_concept',
            'life_skills': 'life_skills'
        }
        
        return subject_map.get(concept.subject, 'general')
    
    def _discover_connections(self, new_concept: Concept) -> List[ConceptConnection]:
        """Discover connections between new concept and existing ones"""
        connections = []
        
        # Get all existing concepts
        existing_concepts = list(self.graph.nodes())
        
        for existing_id in existing_concepts:
            if existing_id == new_concept.id:
                continue
                
            existing_node = self.graph.nodes[existing_id]
            
            # Check for different connection types
            connection_strength = 0.0
            connection_type = None
            
            # 1. Category similarity
            if existing_node['category'] == self._categorize_concept(new_concept):
                connection_strength = max(connection_strength, 0.6)
                connection_type = 'category'
            
            # 2. Emotional context similarity  
            if existing_node['emotional_context'] == new_concept.emotional_context:
                connection_strength = max(connection_strength, 0.5)
                connection_type = 'emotional'
            
            # 3. Content similarity (simple keyword matching)
            content_similarity = self._calculate_content_similarity(
                new_concept.content, existing_node['content']
            )
            if content_similarity > 0.3:
                connection_strength = max(connection_strength, content_similarity)
                connection_type = 'similarity'
            
            # 4. Predefined patterns
            pattern_strength = self._check_pattern_connections(new_concept.id, existing_id)
            if pattern_strength > connection_strength:
                connection_strength = pattern_strength
                connection_type = 'pattern'
            
            # Create connection if strong enough
            if connection_strength > 0.4:
                connection = ConceptConnection(
                    concept1_id=new_concept.id,
                    concept2_id=existing_id,
                    connection_type=connection_type,
                    strength=connection_strength,
                    discovered_through='learning_session'
                )
                
                self.graph.add_edge(
                    new_concept.id, 
                    existing_id,
                    weight=connection_strength,
                    connection_type=connection_type
                )
                
                connections.append(connection)
        
        return connections
    
    def _calculate_content_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity between two concept contents"""
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        # Remove common words
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'can', 'that'}
        words1 = words1 - common_words
        words2 = words2 - common_words
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _check_pattern_connections(self, concept1_id: str, concept2_id: str) -> float:
        """Check if concepts match predefined connection patterns"""
        max_strength = 0.0
        
        for pattern_type, patterns in self.connection_patterns.items():
            for c1, c2, strength in patterns:
                if ((c1 in concept1_id.lower() and c2 in concept2_id.lower()) or 
                    (c2 in concept1_id.lower() and c1 in concept2_id.lower())):
                    max_strength = max(max_strength, strength)
        
        return max_strength
    
    def get_related_concepts(self, concept_id: str, max_distance: int = 2) -> List[Dict]:
        """Get concepts related to the given concept within max_distance"""
        if concept_id not in self.graph:
            return []
        
        related = []
        
        # Get direct neighbors
        for neighbor in self.graph.neighbors(concept_id):
            edge_data = self.graph.edges[concept_id, neighbor]
            node_data = self.graph.nodes[neighbor]
            
            related.append({
                'concept_id': neighbor,
                'content': node_data['content'],
                'connection_strength': edge_data['weight'],
                'connection_type': edge_data['connection_type'],
                'distance': 1
            })
        
        # Get concepts at distance 2 if requested
        if max_distance >= 2:
            for neighbor in self.graph.neighbors(concept_id):
                for second_neighbor in self.graph.neighbors(neighbor):
                    if second_neighbor != concept_id and second_neighbor not in [r['concept_id'] for r in related]:
                        node_data = self.graph.nodes[second_neighbor]
                        
                        related.append({
                            'concept_id': second_neighbor,
                            'content': node_data['content'],
                            'connection_strength': 0.3,  # Indirect connection
                            'connection_type': 'indirect',
                            'distance': 2
                        })
        
        # Sort by connection strength
        related.sort(key=lambda x: x['connection_strength'], reverse=True)
        return related[:10]  # Return top 10
    
    def visualize_concept_network(self, center_concept: Optional[str] = None, 
                                  save_path: Optional[str] = None) -> None:
        """Create a visual representation of Marcus's concept network"""
        plt.figure(figsize=(15, 12))
        
        if center_concept and center_concept in self.graph:
            # Show subgraph around center concept
            subgraph_nodes = set([center_concept])
            subgraph_nodes.update(self.graph.neighbors(center_concept))
            
            # Add second-degree neighbors for richer visualization
            for neighbor in list(subgraph_nodes):
                subgraph_nodes.update(list(self.graph.neighbors(neighbor))[:3])
            
            subgraph = self.graph.subgraph(subgraph_nodes)
        else:
            subgraph = self.graph
        
        # Create layout
        pos = nx.spring_layout(subgraph, k=3, iterations=50)
        
        # Color nodes by category
        category_colors = {
            'emotions': '#FF6B6B',
            'social_skills': '#4ECDC4', 
            'moral_concepts': '#45B7D1',
            'self_concept': '#96CEB4',
            'academic': '#FFEAA7',
            'life_skills': '#DDA0DD',
            'general': '#D3D3D3'
        }
        
        node_colors = []
        for node in subgraph.nodes():
            category = subgraph.nodes[node].get('category', 'general')
            node_colors.append(category_colors.get(category, '#D3D3D3'))
        
        # Draw edges with different styles for connection types
        edge_styles = {
            'category': '-',
            'emotional': '--',
            'similarity': ':',
            'pattern': '-.'
        }
        
        for edge_type in edge_styles:
            edges_of_type = [(u, v) for u, v, d in subgraph.edges(data=True) 
                           if d.get('connection_type') == edge_type]
            if edges_of_type:
                nx.draw_networkx_edges(
                    subgraph, pos, 
                    edgelist=edges_of_type,
                    style=edge_styles[edge_type],
                    alpha=0.6,
                    width=2
                )
        
        # Draw nodes
        nx.draw_networkx_nodes(
            subgraph, pos,
            node_color=node_colors,
            node_size=1000,
            alpha=0.9
        )
        
        # Draw labels
        labels = {node: node.replace('_', '\n') for node in subgraph.nodes()}
        nx.draw_networkx_labels(subgraph, pos, labels, font_size=8, font_weight='bold')
        
        # Add legend
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                    markerfacecolor=color, markersize=10, label=category.replace('_', ' ').title())
                         for category, color in category_colors.items()]
        plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))
        
        plt.title(f"Marcus's Concept Network {f'(centered on {center_concept})' if center_concept else ''}", 
                 fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def get_concept_insights(self, concept_id: str) -> Dict:
        """Get analytical insights about a concept's position in the network"""
        if concept_id not in self.graph:
            return {}
        
        # Calculate various centrality measures
        degree_centrality = nx.degree_centrality(self.graph)[concept_id]
        betweenness_centrality = nx.betweenness_centrality(self.graph)[concept_id]
        
        # Get concept's neighborhood
        neighbors = list(self.graph.neighbors(concept_id))
        
        # Analyze connection types
        connection_types = defaultdict(int)
        for neighbor in neighbors:
            conn_type = self.graph.edges[concept_id, neighbor].get('connection_type', 'unknown')
            connection_types[conn_type] += 1
        
        return {
            'centrality_score': degree_centrality,
            'bridge_score': betweenness_centrality,
            'total_connections': len(neighbors),
            'connection_breakdown': dict(connection_types),
            'most_connected_concepts': neighbors[:5],
            'category': self.graph.nodes[concept_id].get('category', 'unknown'),
            'network_importance': 'high' if degree_centrality > 0.1 else 'medium' if degree_centrality > 0.05 else 'low'
        }
    
    def discover_concept_clusters(self) -> Dict[str, List[str]]:
        """Identify clusters of related concepts"""
        try:
            # Use community detection to find clusters
            communities = nx.community.greedy_modularity_communities(self.graph)
            
            clusters = {}
            for i, community in enumerate(communities):
                cluster_name = f"cluster_{i+1}"
                
                # Try to name cluster based on dominant category
                categories = [self.graph.nodes[node].get('category', 'general') for node in community]
                dominant_category = max(set(categories), key=categories.count)
                
                if categories.count(dominant_category) > len(categories) * 0.6:
                    cluster_name = f"{dominant_category}_cluster"
                
                clusters[cluster_name] = list(community)
            
            return clusters
        except:
            # Fallback: group by category
            clusters = defaultdict(list)
            for node in self.graph.nodes():
                category = self.graph.nodes[node].get('category', 'general')
                clusters[f"{category}_group"].append(node)
            
            return dict(clusters)
    
    def generate_learning_connections_report(self) -> str:
        """Generate a report on how Marcus's concepts are connecting"""
        total_concepts = self.graph.number_of_nodes()
        total_connections = self.graph.number_of_edges()
        
        if total_concepts == 0:
            return "Marcus hasn't learned any concepts yet."
        
        # Calculate network density
        max_possible_connections = total_concepts * (total_concepts - 1) / 2
        density = total_connections / max_possible_connections if max_possible_connections > 0 else 0
        
        # Find most central concepts
        if total_concepts > 1:
            centrality = nx.degree_centrality(self.graph)
            most_central = max(centrality.items(), key=lambda x: x[1])
        else:
            most_central = None
        
        # Analyze clusters
        clusters = self.discover_concept_clusters()
        
        report = f"""
🧠 Marcus's Concept Network Analysis:

📊 Network Statistics:
   • Total concepts learned: {total_concepts}
   • Concept connections formed: {total_connections}
   • Network density: {density:.2%}
   
🌟 Most Connected Concept:
   • {most_central[0] if most_central else 'None yet'}: {most_central[1]:.2%} centrality
   
🔗 Learning Clusters Discovered:
"""
        
        for cluster_name, concepts in clusters.items():
            if len(concepts) > 1:
                report += f"   • {cluster_name}: {len(concepts)} concepts\n"
                report += f"     └─ {', '.join(concepts[:3])}{'...' if len(concepts) > 3 else ''}\n"
        
        report += f"""
💡 Network Insights:
   • Marcus is building {'strong' if density > 0.3 else 'moderate' if density > 0.1 else 'initial'} connections between ideas
   • Learning shows {'high' if len(clusters) > 3 else 'moderate' if len(clusters) > 1 else 'basic'} conceptual organization
   • Concept integration appears {'advanced' if most_central and most_central[1] > 0.2 else 'developing'}
"""
        
        return report.strip()

# Integration with existing Marcus systems
def integrate_concept_graph_with_marcus():
    """Integration function to add concept graphing to existing Marcus"""
    from marcus_memory_system import MarcusMemorySystem
    from marcus_curriculum_system import MarcusCurriculumSystem
    
    # Initialize systems
    memory = MarcusMemorySystem("marcus_with_graph.db")
    curriculum = MarcusCurriculumSystem(memory)
    concept_graph = MarcusConceptGraph(memory)
    
    # Teach Marcus some concepts and build the graph
    print("🧠 Teaching Marcus and building concept graph...")
    
    test_concepts = [
        Concept("friendship", "Friends are people who care about each other", "social_emotional", "kindergarten", "warm"),
        Concept("kindness", "Being kind means helping others and using nice words", "social_emotional", "kindergarten", "caring"),
        Concept("sharing", "Sharing toys and treats makes everyone happy", "social_emotional", "kindergarten", "generous"),
        Concept("empathy", "Understanding how others feel helps me be a good friend", "social_emotional", "kindergarten", "understanding"),
        Concept("counting", "I can count from 1 to 10: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10", "mathematics", "kindergarten", "proud"),
        Concept("colors", "Red, blue, and yellow are primary colors", "art", "kindergarten", "curious"),
        Concept("self_worth", "I am special just the way I am", "self_concept", "kindergarten", "confident")
    ]
    
    # Learn concepts and add to graph
    for concept in test_concepts:
        success = memory.learn_concept(concept)
        if success:
            concept_graph.add_concept_to_graph(concept)
            print(f"✅ Learned and graphed: {concept.id}")
    
    # Show related concepts
    print(f"\n🔗 Concepts related to 'friendship':")
    related = concept_graph.get_related_concepts('friendship')
    for rel in related[:3]:
        print(f"   • {rel['concept_id']}: {rel['connection_strength']:.2f} ({rel['connection_type']})")
    
    # Generate network report
    print(f"\n{concept_graph.generate_learning_connections_report()}")
    
    # Visualize (this will open a plot window)
    print(f"\n📊 Generating visualization...")
    concept_graph.visualize_concept_network(center_concept='friendship', save_path='marcus_concept_network.png')
    
    return concept_graph

# Test the concept graph system
def test_concept_graph():
    """Test the concept graph functionality"""
    print("🧠 Testing Marcus Concept Graph System...")
    
    return integrate_concept_graph_with_marcus()

if __name__ == "__main__":
    concept_graph = test_concept_graph()
    print("🎉 Concept Graph System test completed!")