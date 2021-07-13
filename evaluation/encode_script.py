import argparse

from wav_steganography.wav_file import WAVFile
from pathlib import Path

audio_path = Path(__file__).parent.parent / "audio"
minute_files = audio_path / "1min_files"
audio_files = minute_files.glob("*.wav")


def encode_single_lsb(out, lsb, text):
    """ encode a file into all audio files with a specific number of LSBs converted """
    for audio_file in audio_files:
        encode_file(audio_file, f"{out}/modified_{audio_file.name}", lsb, text)


def encode_all_lsb(text):
    """ encode a file into all audio files, iterate over all LSBs possible """
    for number_of_lsb in range(1, 16):
        print(f"\n----- Number of LSBs used for encoding: {number_of_lsb} -----\n")

        lsb_directory = f"lsb_{number_of_lsb}"
        output = audio_path / "evaluation_samples" / lsb_directory
        output.mkdir(exist_ok=True, parents=True)

        encode_single_lsb(output, number_of_lsb, text)


def encode_file(input_dir, output, lsb, text_to_encode):
    print(f"I: {input_dir}")
    print(f"O: {output}\n")
    wav_file = WAVFile(input_dir)
    wav_file.encode(text_to_encode, least_significant_bits=lsb)
    wav_file.write(output, overwrite=True)


def parse_args():
    parser = argparse.ArgumentParser(description="start the encode script")
    default_encode_text_path = audio_path / "txt_files" / "100.txt"
    parser.add_argument("--encode", type=str, default=default_encode_text_path, help="name of the encode txt-file")
    parser.add_argument("--single", action="store_true",
                        help="encode a txt file into all samples, with a specific number of LSBs converted")
    parser.add_argument("-l", "--lsb", type=int, help="sets the number of LSBs used for single file encoding")
    parser.add_argument("-o", "--output", type=str, help="name of the output directory")
    parser.add_argument("--all", action="store_true",
                        help="encode a txt file into all samples, iterate over all possible LSBs")

    return parser.parse_args()


def main():
    args = parse_args()

    text_to_encode_file_path = audio_path / "txt_files" / args.encode
    print(f"E: {text_to_encode_file_path}\n")

    with text_to_encode_file_path.open() as text_file:
        text = text_file.read().encode("UTF-8")

        if args.single:
            output_directory = audio_path / "evaluation_samples" / args.output
            output_directory.mkdir(exist_ok=True)
            encode_single_lsb(output_directory, args.lsb, text)

        if args.all:
            encode_all_lsb(text)


if __name__ == "__main__":
    main()
