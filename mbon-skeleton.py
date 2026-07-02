## set up packages
import navis
from fafbseg import flywire
flywire.set_default_dataset("public")

#downloading MBON skeletons and appending them into one .obj file
print("Searching for Mushroom Body Output Neurons...")
mbon_criteria = flywire.NeuronCriteria(type="MBON17", regex=True) #replace type with MBON of choice

print("Downloading skeletons...")
mbon_skeletons = flywire.get_skeletons(mbon_criteria)
print(f"Successfully retrieved {len(mbon_skeletons)} MBONs!")

output_file = "MBON_#.obj"
print(f"Writing all neurons into {output_file}...")

# Open a single file to write the 3D lines
with open(output_file, 'w') as f:
    f.write("# OBJ file containing combined MBON skeletons\n")
    vertex_offset = 1  # OBJ files use 1-based indexing

    for neuron in mbon_skeletons:
        f.write(f"g neuron_{neuron.id}\n")  # Group each neuron by its FlyWire ID
        
        # 1. Write the 3D positions (Vertices)
        nodes = neuron.nodes[['x', 'y', 'z']].values
        for vertex in nodes:
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        
        # 2. Map the structural connections (Lines)
        node_id_to_index = {node_id: i + vertex_offset for i, node_id in enumerate(neuron.nodes['node_id'].values)}
        for edge in neuron.edges:
            if edge[0] in node_id_to_index and edge[1] in node_id_to_index:
                f.write(f"l {node_id_to_index[edge[0]]} {node_id_to_index[edge[1]]}\n")
                
        # Move the index offset forward for the next neuron
        vertex_offset += len(nodes)

print(f"Success! Your master file has been created at: '{output_file}'")