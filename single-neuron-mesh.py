import navis
from fafbseg import flywire

# flywire.set_chunkedgraph_secret("insert token here")
flywire.set_default_dataset("public") # sets default dataset to public, no additional access token is required

print("Searching for neurons ...")
neuron_criteria = flywire.NeuronCriteria(type="^PPL104$", regex=True) # this is the only line you need to change!

print("Downloading 3D mesh ...")
neuron_meshes = flywire.get_mesh_neuron(neuron_criteria)

print("Downloading 3D mesh...")
# get_mesh_neuron returns a NeuronList
neuron_meshes = flywire.get_mesh_neuron(neuron_criteria)

if len(neuron_meshes) > 0:
    print(f"Successfully retrieved {len(neuron_meshes)} exact neuron(s)!")
    
    # Loop through each individual neuron in the collection
    for neuron in neuron_meshes:
        # Use the unique FlyWire ID in the filename so they don't overwrite each other
        output_file = f"neuronID_{neuron.id}.obj"
        print(f"Saving mesh to {output_file}...")
        
        # Save this specific individual neuron
        navis.write_mesh(neuron, output_file)
        
    print("Success! All individual meshes have been saved.")
else:
    print("Error: No neurons found matching the exact criteria.")
