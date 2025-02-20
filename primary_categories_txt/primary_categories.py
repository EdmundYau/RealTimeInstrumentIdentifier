import os
import yaml

# Load instrument group mappings
def load_instrument_groups(mapping_file):
    group_map = {}
    with open(mapping_file, "r") as f:
        for line in f:
            parts = line.strip().split(" ", 1)
            if len(parts) == 2:
                group_map[parts[1]] = parts[0]
    return group_map

instrument_groups = load_instrument_groups("instrument_groups.txt")

# ===================== FOR EACH TRACK =====================
def extract_general_categories(track_path):
    metadata_path = os.path.join(track_path, "metadata.yaml")
    if not os.path.exists(metadata_path):
        return None 

    with open(metadata_path, "r") as file:
        metadata = yaml.safe_load(file)

    # Extract general categories
    output = f"Track: {track_path}\n"
    valid_entries = []

    for stem_id, stem_data in metadata.get("stems", {}).items():
        if not stem_data.get("audio_rendered", True): 
            continue  
        inst_class = stem_data.get("inst_class", "Unknown")
        inst_class_number = instrument_groups.get(inst_class, "Unknown")
        valid_entries.append(f"{stem_id}.flac: {inst_class_number}")

    if valid_entries:
        output += "\n".join(valid_entries) + "\n"
        return output
    
    return None  

# ===================== FOR EACH FOLDER =====================
def process_all_tracks(dataset_path, output_file):
    track_dirs = [os.path.join(dataset_path, d) for d in os.listdir(dataset_path) if d.startswith("Track")]

    with open(output_file, "w") as f:
        for track in track_dirs:
            result = extract_general_categories(track)
            if result:
                f.write(result)

# Generate general category files
process_all_tracks("slakh2100_flac_redux/train", "primary_categories_train.txt")
process_all_tracks("slakh2100_flac_redux/validation", "primary_categories_validation.txt")
process_all_tracks("slakh2100_flac_redux/test", "primary_categories_test.txt")
