# Import Libraries
import os
import yaml  

# ===================== FOR EACH TRACK =====================
def extract_program_numbers(track_path):
    metadata_path = os.path.join(track_path, "metadata.yaml")
    if not os.path.exists(metadata_path):
        return None 

    with open(metadata_path, "r") as file:
        metadata = yaml.safe_load(file)

    # Extract program numbers
    output = f"Track: {track_path}\n"
    for stem_id, stem_data in metadata.get("stems", {}).items():
        program_num = stem_data.get("program_num", "Unknown")  
        output += f"{stem_id}.flac: {program_num}\n"

    return output

# ===================== FOR EACH FOLDER =====================
def process_all_tracks(dataset_path, output_file):
    track_dirs = [os.path.join(dataset_path, d) for d in os.listdir(dataset_path) if d.startswith("Track")]

    with open(output_file, "w") as f:
        for track in track_dirs:
            result = extract_program_numbers(track)
            if result:
                f.write(result)

# Generate category files (~30–60 secs)
process_all_tracks("slakh2100_flac_redux/train", "categories_train.txt")
process_all_tracks("slakh2100_flac_redux/validation", "categories_validation.txt")
process_all_tracks("slakh2100_flac_redux/test", "categories_test.txt")
