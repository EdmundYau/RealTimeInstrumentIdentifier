# Import Libraries
import numpy as np
import librosa
import os
import concurrent.futures
from tqdm import tqdm


# ===================== FOR EACH STEM =====================
def detect_active_timestamps(stem_path, sr=44100, threshold=0.005):
    # Load and compute energy
    y, sr = librosa.load(stem_path, sr=sr)  
    rms = librosa.feature.rms(y=y)[0] 
    
    # Find all activity times
    active_frames = np.where(rms > threshold)[0] 
    active_times = librosa.frames_to_time(active_frames, sr=sr)  
    if len(active_times) == 0:
        return []
    
    # Mark activity times into timestamps
    timestamps = []
    start_time = active_times[0]
    
    for i in range(1, len(active_times)):
        if active_times[i] - active_times[i-1] > 0.3:  # Gap (secs)
            timestamps.append((float(round(start_time, 2)), float(round(active_times[i-1], 2))))
            start_time = active_times[i]
    timestamps.append((float(round(start_time, 2)), float(round(active_times[-1], 2))))
    
    return timestamps


# ===================== FOR EACH TRACK =====================
def process_all_stems(track):
    stems_dir = os.path.join(track, "stems")
    if not os.path.exists(stems_dir):
        return None  
    
    # Iterate stems and list timestamps
    output = f"Track: {track}\n"
    for stem in os.listdir(stems_dir):
        stem_path = os.path.join(stems_dir, stem)
        timestamps = detect_active_timestamps(stem_path)
        output += f"{stem}: {timestamps}\n"
    return output


# ===================== FOR EACH FOLDER =====================
def process_all_tracks(dataset_path, output_file):
    track_dirs = [os.path.join(dataset_path, d) for d in os.listdir(dataset_path) if d.startswith("Track")]

    # ThreadPoolExecutor for parallel processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor, open(output_file, "w") as f:
        results = list(tqdm(executor.map(process_all_stems, track_dirs), total=len(track_dirs), desc="Processing Tracks"))
        
        for result in results:
            if result:
                f.write(result)
            
            
# Compiling RAW timestamps (~20–30 min)
process_all_tracks("slakh2100_flac_redux/reduced_test", "raw_timestamps_reduced_test.txt")
