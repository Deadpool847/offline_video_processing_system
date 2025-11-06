"""Command-line interface."""

import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from core.pipeline import Pipeline
from core.presets import PresetManager
from core.logging_config import setup_logging
from stylizers import *


def render_command(args):
    """Render videos with styles."""
    print(f"Rendering: {args.input}")
    print(f"Styles: {args.styles}")
    print(f"Preset: {args.preset}")
    print(f"Output: {args.out}")
    
    # TODO: Implement full rendering
    print("\nRendering functionality ready for implementation")


def preview_command(args):
    """Generate preview."""
    print(f"Previewing: {args.input}")
    print(f"Style: {args.style}")
    print(f"Start: {args.start}")
    print(f"Duration: {args.dur}")
    
    # TODO: Implement preview
    print("\nPreview functionality ready for implementation")


def train_command(args):
    """Train/fine-tune models."""
    print(f"Training data: {args.data}")
    print(f"Epochs: {args.epochs}")
    print(f"Export path: {args.export}")
    
    # TODO: Implement training
    print("\nTraining functionality ready for implementation")


def main():
    parser = argparse.ArgumentParser(description="ML-Powered Video Producer")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Render command
    render_parser = subparsers.add_parser('render', help='Render videos')
    render_parser.add_argument('--in', dest='input', required=True, help='Input file or folder')
    render_parser.add_argument('--styles', required=True, help='Comma-separated styles')
    render_parser.add_argument('--preset', default='Balanced', help='Quality preset')
    render_parser.add_argument('--out', required=True, help='Output directory')
    
    # Preview command
    preview_parser = subparsers.add_parser('preview', help='Generate preview')
    preview_parser.add_argument('--in', dest='input', required=True, help='Input video')
    preview_parser.add_argument('--style', required=True, help='Style to preview')
    preview_parser.add_argument('--start', default='00:00:10', help='Start time')
    preview_parser.add_argument('--dur', default='8s', help='Duration')
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Train models')
    train_parser.add_argument('--data', required=True, help='Training data directory')
    train_parser.add_argument('--epochs', type=int, default=1, help='Number of epochs')
    train_parser.add_argument('--export', required=True, help='Export path for ONNX')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    if args.command == 'render':
        render_command(args)
    elif args.command == 'preview':
        preview_command(args)
    elif args.command == 'train':
        train_command(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()