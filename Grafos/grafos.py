import networkx as nx
import matplotlib.pyplot as plt
import csv

# Load data
with open('software_dev.csv', 'r') as f:
    reader = csv.DictReader(f)
    devs = [row for row in reader]
    # Clean keys
    devs = [{k.strip(): v for k, v in d.items()} for d in devs]

print("=" * 70)
print("SOFTWARE DEVELOPER NETWORK ANALYSIS")
print("=" * 70)

# ============================================================================
# GRAPH 1: Developer Similarity Network
# ============================================================================
print("\n1. DEVELOPER SIMILARITY NETWORK")
G_sim = nx.Graph()

# Add nodes with attributes
for d in devs:
    G_sim.add_node(int(d['Dev_ID']), lang=d['Lenguaje_Principal'], 
                   exp=int(d['Experiencia_Anios']), sat=int(d['Satisfaccion']))

# Create edges based on similarity
for i, d1 in enumerate(devs):
    for d2 in devs[i+1:]:
        score = 0
        if d1['Lenguaje_Principal'] == d2['Lenguaje_Principal']:
            score += 3
        if abs(int(d1['Experiencia_Anios']) - int(d2['Experiencia_Anios'])) <= 2:
            score += 2
        if abs(int(d1['Satisfaccion']) - int(d2['Satisfaccion'])) <= 1:
            score += 1
        if score >= 4:
            G_sim.add_edge(int(d1['Dev_ID']), int(d2['Dev_ID']), weight=score)

print(f"Developers: {G_sim.number_of_nodes()}")
print(f"Similar pairs: {G_sim.number_of_edges()}")
print(f"Communities: {nx.number_connected_components(G_sim)}")

# ============================================================================
# GRAPH 2: Language-Experience Bipartite Graph
# ============================================================================
print("\n2. LANGUAGE-EXPERIENCE BIPARTITE GRAPH")
G_bi = nx.Graph()

# Categorize experience
for d in devs:
    exp = int(d['Experiencia_Anios'])
    d['exp_level'] = 'Junior' if exp <= 3 else 'Mid' if exp <= 6 else 'Senior'

# Add nodes
langs = set(d['Lenguaje_Principal'] for d in devs)
levels = set(d['exp_level'] for d in devs)

for lang in langs:
    G_bi.add_node(f"L_{lang}", bipartite=0)
for level in levels:
    G_bi.add_node(f"E_{level}", bipartite=1)

# Add weighted edges
for lang in langs:
    for level in levels:
        count = sum(1 for d in devs if d['Lenguaje_Principal'] == lang and d['exp_level'] == level)
        if count > 0:
            G_bi.add_edge(f"L_{lang}", f"E_{level}", weight=count)

print(f"Languages: {len(langs)}, Experience levels: {len(levels)}")
print(f"Connections: {G_bi.number_of_edges()}")

# ============================================================================
# GRAPH 3: Performance Dependency Graph (Directed)
# ============================================================================
print("\n3. PERFORMANCE DEPENDENCY GRAPH")
G_perf = nx.DiGraph()

factors = ['Experience', 'Certifications', 'Hours', 'Code_Output', 
           'Bug_Rate', 'Satisfaction']
G_perf.add_nodes_from(factors)

# Dependencies: (from, to, weight, positive/negative)
deps = [
    ('Experience', 'Bug_Rate', 0.3, 'neg'),
    ('Experience', 'Code_Output', 0.2, 'pos'),
    ('Experience', 'Satisfaction', 0.25, 'pos'),
    ('Certifications', 'Code_Output', 0.15, 'pos'),
    ('Certifications', 'Bug_Rate', 0.2, 'neg'),
    ('Hours', 'Code_Output', 0.5, 'pos'),
    ('Hours', 'Bug_Rate', 0.3, 'pos'),
    ('Hours', 'Satisfaction', 0.4, 'neg'),
    ('Bug_Rate', 'Satisfaction', 0.35, 'neg'),
    ('Code_Output', 'Satisfaction', 0.1, 'pos'),
]

for src, tgt, w, inf in deps:
    G_perf.add_edge(src, tgt, weight=w, influence=inf)

print(f"Factors: {G_perf.number_of_nodes()}")
print(f"Dependencies: {G_perf.number_of_edges()}")

# ============================================================================
# VISUALIZATION
# ============================================================================
print("\n4. GENERATING VISUALIZATIONS")
fig, axes = plt.subplots(2, 2, figsize=(16, 14))
fig.suptitle('Software Developer Network Analysis', fontsize=16, fontweight='bold')

# Plot 1: Similarity Network
colors = {'Python': '#3776ab', 'Java': '#f89820', 'C#': '#68217a', 'R': '#276dc3'}
node_colors = [colors[G_sim.nodes[n]['lang']] for n in G_sim.nodes()]
pos1 = nx.spring_layout(G_sim, k=0.5, seed=42)
nx.draw(G_sim, pos1, node_color=node_colors, node_size=300, with_labels=True,
        font_size=8, font_weight='bold', edge_color='gray', alpha=0.7, ax=axes[0,0])
axes[0,0].set_title('Developer Similarity Network\n(Colored by Language)', fontweight='bold')
legend_handles = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=c,
               markersize=10, label=l)
    for l, c in colors.items()
]
axes[0,0].legend(handles=legend_handles, loc='upper right', fontsize=8)

# Plot 2: Bipartite Graph
lang_nodes = [n for n in G_bi.nodes() if n.startswith('L_')]
exp_nodes = [n for n in G_bi.nodes() if n.startswith('E_')]
pos2 = {**{n: (0, i*2) for i, n in enumerate(lang_nodes)},
        **{n: (3, i*2.5) for i, n in enumerate(exp_nodes)}}
weights = [G_bi[u][v]['weight'] for u, v in G_bi.edges()]

nx.draw_networkx_nodes(G_bi, pos2, lang_nodes, node_color='lightblue', 
                       node_size=800, node_shape='s', ax=axes[0,1])
nx.draw_networkx_nodes(G_bi, pos2, exp_nodes, node_color='lightcoral', 
                       node_size=800, node_shape='o', ax=axes[0,1])
nx.draw_networkx_edges(G_bi, pos2, width=[w*0.5 for w in weights], alpha=0.5, ax=axes[0,1])
nx.draw_networkx_labels(G_bi, pos2, {n: n.split('_')[1] for n in G_bi.nodes()},
                       font_size=9, ax=axes[0,1])
axes[0,1].set_title('Language-Experience Distribution\n(Edge width = dev count)', 
                    fontweight='bold')
axes[0,1].axis('off')

# Plot 3: Performance Dependencies
pos3 = nx.spring_layout(G_perf, k=1.5, seed=42)
edge_colors = ['green' if G_perf[u][v]['influence'] == 'pos' else 'red' 
               for u, v in G_perf.edges()]
edge_widths = [G_perf[u][v]['weight']*5 for u, v in G_perf.edges()]
nx.draw(G_perf, pos3, node_color='lightgreen', node_size=2000, with_labels=True,
        font_size=9, font_weight='bold', edge_color=edge_colors, width=edge_widths,
        arrows=True, arrowsize=20, connectionstyle='arc3,rad=0.1', ax=axes[1,0])
axes[1,0].set_title('Performance Dependencies\n(Green=Positive, Red=Negative)', 
                    fontweight='bold')

# Plot 4: Statistics Table
stats = [
    ['Total Developers', len(devs)],
    ['Languages', len(langs)],
    ['Avg Experience', f"{sum(int(d['Experiencia_Anios']) for d in devs)/len(devs):.1f}"],
    ['Avg Satisfaction', f"{sum(int(d['Satisfaccion']) for d in devs)/len(devs):.1f}"],
    ['Similar Pairs', G_sim.number_of_edges()],
    ['Performance Factors', G_perf.number_of_nodes()]
]
axes[1,1].axis('off')
table = axes[1,1].table(cellText=stats, colLabels=['Metric', 'Value'],
                        cellLoc='left', loc='center', colWidths=[0.6, 0.3])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
for i in range(2):
    table[(0, i)].set_facecolor('#4CAF50')
    table[(0, i)].set_text_props(weight='bold', color='white')
axes[1,1].set_title('Network Statistics', fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('developer_network_analysis.png', dpi=300, bbox_inches='tight')
print("Saved: developer_network_analysis.png")

# Advanced Metrics
if G_sim.number_of_edges() > 0:
    print("\n5. TOP CONNECTED DEVELOPERS (Hubs)")
    cent = nx.degree_centrality(G_sim)
    for dev_id, score in sorted(cent.items(), key=lambda x: x[1], reverse=True)[:3]:
        dev = next(d for d in devs if int(d['Dev_ID']) == dev_id)
        print(f"  Dev {dev_id}: {dev['Lenguaje_Principal']}, "
              f"{dev['Experiencia_Anios']} years, Centrality: {score:.3f}")
    print(f"\nClustering coefficient: {nx.average_clustering(G_sim):.3f}")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
plt.show()
