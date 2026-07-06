# remember to install fafbseg by using the command pip3 install fafbseg in your terminal
import navis
import trimesh
import fast_simplification
from fafbseg import flywire

# flywire.set_chunkedgraph_secret("insert token here")
flywire.set_default_dataset("public") # sets default dataset to public, no additional access token is required

print("Searching for neurons ...")
neuron_criteria = flywire.NeuronCriteria(type="^KCapbp-m$", side="right", regex=True)

print("Downloading 3D meshes (LOD 3)...")
neuron_meshes = flywire.get_mesh_neuron(neuron_criteria, lod=3)
print(f"Successfully retrieved {len(neuron_meshes)} meshes!")

output_file = "neuronID_compressed.obj"
print("Processing and aggressively compressing individual meshes...")

trimesh_list = []
for idx, neuron in enumerate(neuron_meshes):
    verts, faces = neuron.vertices, neuron.faces

    if verts is not None and faces is not None:
        mesh_piece = trimesh.Trimesh(vertices=verts, faces=faces)
        
        # Pre-decimate each individual piece using the fast direct method
        try:
            # 0.90 target_reduction means remove 90% of faces, keep 10%
            v_out, f_out = fast_simplification.simplify(mesh_piece.vertices, mesh_piece.faces, target_reduction=0.90)
            mesh_piece = trimesh.Trimesh(vertices=v_out, faces=f_out)
        except Exception:
            pass 
            
        trimesh_list.append(mesh_piece)

if trimesh_list:
    print("Fusing all optimized meshes into one master object...")
    combined_trimesh = trimesh.util.concatenate(trimesh_list)
    
    print("Performing final cluster compression down to 10% total volume...")
    # target_reduction=0.90 removes 90% of the combined overlapping faces
    v_final, f_final = fast_simplification.simplify(
        combined_trimesh.vertices, 
        combined_trimesh.faces, 
        target_reduction=0.90
    )
    
    compressed_mesh = trimesh.Trimesh(vertices=v_final, faces=f_final)
    
    print(f"Saving optimized model to {output_file}...")
    compressed_mesh.export(output_file)
    print("Success! Your highly optimized mesh bundle is ready.")
else:
    print("Error: Could not extract mesh data.")
