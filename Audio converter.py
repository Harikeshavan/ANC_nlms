import wave, os.path as pth, struct, os

# Define directories
inp_noise_path = './Wav Files/noise ref'
inp_signal_path = './Wav Files/noisy sig'
raw_noise_path = './Raw audio/noise ref'
raw_signal_path = './Raw audio/noisy sig'
mem_noise_path = './Mem Files/noise ref'
mem_signal_path = './Mem Files/noisy sig'

chunk_size = 1000000  # samples per mem file

# Mapping file types to their respective paths
PATHS = {
    "noise": {
        "inp": inp_noise_path,
        "raw": raw_noise_path,
        "mem": mem_noise_path
    },
    "signal": {
        "inp": inp_signal_path,
        "raw": raw_signal_path,
        "mem": mem_signal_path
    }
}

def process_wav(nme, file_type):
    # Select correct paths
    inp_path = PATHS[file_type]["inp"]
    raw_path = PATHS[file_type]["raw"]
    mem_path = PATHS[file_type]["mem"]

    # Build filenames
    ip_file = pth.join(inp_path, nme + ".wav")
    op_raw_file = pth.join(raw_path, nme + ".raw")
    op_txt_file = pth.join(mem_path, nme + ".txt")

    # Load wav
    with wave.open(ip_file, "rb") as wav:
        assert wav.getnchannels() == 2
        assert wav.getsampwidth() == 2
        assert wav.getframerate() == 48000
        data = wav.readframes(wav.getnframes())

    # Save raw binary
    os.makedirs(raw_path, exist_ok=True)
    with open(op_raw_file, "wb") as f:
        f.write(data)

    # Split into chunks
    samples = []
    mem_file_num = 1
    with open(op_raw_file, "rb") as raw_file:
        while True:
            chunk_samples = []
            for _ in range(chunk_size):
                sample_bytes = raw_file.read(2)
                if not sample_bytes:
                    break
                sample = struct.unpack("<h", sample_bytes)[0]
                chunk_samples.append(sample)
                samples.append(sample)

            if not chunk_samples:
                break

            mem_subfolder = pth.join(mem_path, f"{nme}")
            os.makedirs(mem_subfolder, exist_ok=True)
            op_mem_file = pth.join(mem_subfolder, f"{nme}_{mem_file_num}.mem")

            if len(chunk_samples) < chunk_size:
                chunk_samples.extend([0] * (chunk_size - len(chunk_samples)))

            with open(op_mem_file, "w") as mem_file:
                for s in chunk_samples:
                    mem_file.write(f"{s & 0xFFFF:04x}\n")

            mem_file_num += 1

    # Save .txt file with signed values
    os.makedirs(mem_path, exist_ok=True)
    with open(op_txt_file, "w") as txt:
        txt.write(f"Total samples: {len(samples)}\n")
        for s in samples:
            txt.write(f"{s}\n")

    print(f"[{file_type}] Total samples: {len(samples)}")
    print(f"[{file_type}] Total .mem files written: {mem_file_num - 1}")

def process_both(nme):
    for file_type in ["noise", "signal"]:
        process_wav(nme, file_type)

# Example usage
nme = input("Enter file name (without extension): ")
process_both(nme)