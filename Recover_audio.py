import wave
import struct
import math

nme = input("nme: ")

def mem_to_wav(mem_file, wav_file, sample_rate=48000):
    samples = []

    with open(mem_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("//"):
                continue

            if line.lower() == "xxxx":
                val = 0
            else:
                val = int(line, 16)
                if val >= 0x8000:
                    val -= 0x10000

            samples.append(val)

    # Reduce by -10 dB
    scale = 10 ** (-20 / 20)  # ≈ 0.3162
    samples = [int(s * scale) for s in samples]

    # Simple smoothing (3-point moving average)
    smoothed = []
    for i in range(len(samples)):
        if i == 0:
            smoothed.append(int((samples[i] + samples[i+1]) / 2))
        elif i == len(samples)-1:
            smoothed.append(int((samples[i-1] + samples[i]) / 2))
        else:
            smoothed.append(int((samples[i-1] + samples[i] + samples[i+1]) / 3))
    samples = smoothed

    # Write WAV
    with wave.open(wav_file, "wb") as wav:
        wav.setnchannels(2)        # stereo
        wav.setsampwidth(2)        # 16-bit
        wav.setframerate(sample_rate)
        wav.writeframes(b''.join(struct.pack("<h", s) for s in samples))

    print(f"Converted {len(samples)} samples from {mem_file} to {wav_file}")

# Example usage
mem_to_wav("./Mem Files/out file/1.mem", f"./Reconstructed audio/{nme}.wav")