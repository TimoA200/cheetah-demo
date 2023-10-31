import os
from dotenv import load_dotenv

load_dotenv()
from pvrecorder import PvRecorder
import pvcheetah

PV_ACCESS_KEY = os.getenv("PV_ACCESS_KEY")


def main():
    cheetah = pvcheetah.create(access_key=PV_ACCESS_KEY)
    recorder = PvRecorder(device_index=5, frame_length=cheetah.frame_length)

    devices = recorder.get_available_devices()
    print("Available audio devices:")
    for i, device in enumerate(devices):
        print(f"{i}: {device}")

    try:
        recorder.start()

        print("Start recording...")
        while True:
            pcm = recorder.read()
            partial_transcript, is_endpoint = cheetah.process(pcm)

            if partial_transcript:
                print(partial_transcript, end="", flush=True)

            if is_endpoint:
                final_transcript = cheetah.flush()
                print(final_transcript)
                break
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        recorder.delete()
        cheetah.delete()


if __name__ == "__main__":
    main()
