import sys
import librosa
import argparse

class VoicePreprocesser(object):
    """
    """

    def __init__(self):
        super().__init__()
        self.sample_rate = 16000
        self.top_db =20

    def trim(self, fpath):
        # Loading sound file
        y, sr = librosa.load(fpath, sr=self.sample_rate)
        # Trimming
        y, _ = librosa.effects.trim(y, top_db=self.top_db)
        return y

    def trim_file(self, fpath, out_fpath):
        y = self.trim(fpath)
        librosa.output.write_wav(out_fpath, y, self.sample_rate)




_examples = '''examples:

  # enroll a speaker voice
  python %(prog)s enroll --model=given-modelname.model filename.wav

  # verify with a given model name and a arbitoray speaker voice
  python %(prog)s verify --model=given-modelname.model filename.wav

'''

def main():
    parser = argparse.ArgumentParser(
        description='''Voice Preprocess.

Run 'python %(prog)s <subcommand> --help' for subcommand help.''',
        epilog=_examples,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(help='Sub-commands', dest='command')

    parser_trim = subparsers.add_parser('trim', help='trim voice')
    parser_trim.add_argument('--input', type=str, help='input .wav file')
    parser_trim.add_argument('--output', type=str, help='output trimed .wav file')
    
    # parser_verify = subparsers.add_parser('verify', help='verify speaker voice')
    # parser_verify.add_argument('--model', type=str, default='default.model', help='model name used to save speaker model')
    # parser_verify.add_argument('filename', type=str, help='List of random seeds', required=True)

    args = parser.parse_args()
    kwargs = vars(args)
    subcmd = kwargs.pop('command')

    prep = VoicePreprocesser()

    if subcmd == 'trim':
        prep.trim_file(args.input, args.output)
    else:
        print ('Error: unknown subcommand.  Re-run with --help for usage.')
        sys.exit(1)
    
if __name__ == "__main__":
    main()