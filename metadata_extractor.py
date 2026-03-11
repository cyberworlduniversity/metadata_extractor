#!/usr/bin/env python3
"""
Metadata Extractor Tool 🧾
Extracts hidden metadata from image files including camera, date, and GPS location data.
GitHub: hemanathan115
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
except ImportError:
    print("Installing required packages...")
    os.system("pip install Pillow --break-system-packages -q")
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS

try:
    import exifread
except ImportError:
    os.system("pip install exifread --break-system-packages -q")
    import exifread


def get_decimal_coordinates(gps_info):
    """Convert GPS coordinates from DMS to decimal format."""
    def dms_to_decimal(dms, ref):
        degrees = float(dms[0])
        minutes = float(dms[1]) / 60
        seconds = float(dms[2]) / 3600
        decimal = degrees + minutes + seconds
        if ref in ['S', 'W']:
            decimal = -decimal
        return round(decimal, 6)

    try:
        lat = dms_to_decimal(gps_info.get('GPSLatitude', [0, 0, 0]),
                             gps_info.get('GPSLatitudeRef', 'N'))
        lon = dms_to_decimal(gps_info.get('GPSLongitude', [0, 0, 0]),
                             gps_info.get('GPSLongitudeRef', 'E'))
        return lat, lon
    except Exception:
        return None, None


def extract_gps_info(exif_data):
    """Extract and parse GPS information from EXIF data."""
    gps_info = {}
    raw_gps = exif_data.get('GPSInfo', {})
    if not raw_gps:
        return None

    for key, val in raw_gps.items():
        tag_name = GPSTAGS.get(key, key)
        if isinstance(val, tuple):
            val = [float(v) if hasattr(v, 'numerator') else v for v in val]
        gps_info[tag_name] = val

    lat, lon = get_decimal_coordinates(gps_info)
    if lat and lon:
        gps_info['DecimalLatitude'] = lat
        gps_info['DecimalLongitude'] = lon
        gps_info['GoogleMapsLink'] = f"https://www.google.com/maps?q={lat},{lon}"

    return gps_info


def extract_metadata(image_path):
    """Extract all metadata from an image file."""
    path = Path(image_path)
    if not path.exists():
        return {"error": f"File not found: {image_path}"}

    result = {
        "file_info": {
            "filename": path.name,
            "filepath": str(path.resolve()),
            "extension": path.suffix.upper(),
            "file_size": f"{path.stat().st_size / 1024:.2f} KB",
            "last_modified": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        },
        "camera_info": {},
        "date_info": {},
        "gps_info": {},
        "image_info": {},
        "other_metadata": {}
    }

    try:
        img = Image.open(image_path)
        result["image_info"] = {
            "format": img.format,
            "mode": img.mode,
            "width": img.width,
            "height": img.height,
            "resolution": f"{img.width} x {img.height} pixels"
        }

        exif_data = {}
        raw_exif = img._getexif() if hasattr(img, '_getexif') else None
        if raw_exif:
            for tag_id, value in raw_exif.items():
                tag = TAGS.get(tag_id, tag_id)
                exif_data[tag] = value

        # Camera Information
        camera_fields = ['Make', 'Model', 'Software', 'LensModel', 'LensMake',
                         'FocalLength', 'FNumber', 'ExposureTime', 'ISOSpeedRatings',
                         'Flash', 'WhiteBalance', 'ExposureMode', 'MeteringMode']
        for field in camera_fields:
            val = exif_data.get(field)
            if val is not None:
                if hasattr(val, 'numerator'):
                    val = float(val)
                result["camera_info"][field] = str(val)

        # Date Information
        date_fields = ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized']
        for field in date_fields:
            val = exif_data.get(field)
            if val:
                result["date_info"][field] = val

        # GPS Information
        gps = extract_gps_info(exif_data)
        if gps:
            result["gps_info"] = {k: str(v) for k, v in gps.items()}
        else:
            result["gps_info"] = {"status": "No GPS data found"}

        # Other metadata
        skip = set(camera_fields + date_fields + ['GPSInfo', 'MakerNote', 'UserComment'])
        for tag, val in exif_data.items():
            if tag not in skip and not isinstance(val, bytes):
                if hasattr(val, 'numerator'):
                    val = float(val)
                result["other_metadata"][str(tag)] = str(val)[:200]

    except Exception as e:
        result["error"] = f"Could not read EXIF data: {str(e)}"

    return result


def display_metadata(metadata, output_format='pretty'):
    """Display metadata in a formatted way."""
    if output_format == 'json':
        print(json.dumps(metadata, indent=2))
        return

    print("\n" + "="*60)
    print("🧾  METADATA EXTRACTOR - RESULTS")
    print("="*60)

    if "error" in metadata:
        print(f"❌ Error: {metadata['error']}")
        return

    sections = {
        "📁 File Information": "file_info",
        "📷 Camera Information": "camera_info",
        "📅 Date & Time": "date_info",
        "📍 GPS / Location": "gps_info",
        "🖼️  Image Properties": "image_info",
        "ℹ️  Other Metadata": "other_metadata"
    }

    for title, key in sections.items():
        data = metadata.get(key, {})
        if data:
            print(f"\n{title}")
            print("-" * 40)
            for k, v in data.items():
                print(f"  {k:<25} : {v}")

    print("\n" + "="*60)
    print("✅ Extraction Complete!")
    print("="*60 + "\n")


def save_report(metadata, output_path):
    """Save metadata report as JSON file."""
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"📄 Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='🧾 Metadata Extractor - Extract hidden metadata from image files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python metadata_extractor.py photo.jpg
  python metadata_extractor.py photo.jpg --format json
  python metadata_extractor.py photo.jpg --save report.json
  python metadata_extractor.py *.jpg --batch
        """
    )
    parser.add_argument('images', nargs='+', help='Image file(s) to analyze')
    parser.add_argument('--format', choices=['pretty', 'json'], default='pretty',
                        help='Output format (default: pretty)')
    parser.add_argument('--save', metavar='OUTPUT', help='Save report as JSON file')
    parser.add_argument('--batch', action='store_true', help='Process multiple files')

    args = parser.parse_args()

    all_results = {}

    for image_path in args.images:
        print(f"\n🔍 Processing: {image_path}")
        metadata = extract_metadata(image_path)
        all_results[image_path] = metadata

        if not args.batch or len(args.images) == 1:
            display_metadata(metadata, args.format)

    if args.batch and len(args.images) > 1:
        print(f"\n📊 Batch Summary: Processed {len(args.images)} files")
        for path, meta in all_results.items():
            cam = meta.get('camera_info', {})
            date = meta.get('date_info', {})
            gps = meta.get('gps_info', {})
            print(f"\n  📸 {path}")
            print(f"     Camera : {cam.get('Make', 'N/A')} {cam.get('Model', '')}")
            print(f"     Date   : {date.get('DateTimeOriginal', 'N/A')}")
            print(f"     GPS    : {gps.get('DecimalLatitude', 'N/A')}, {gps.get('DecimalLongitude', '')}")

    if args.save:
        save_report(all_results if len(args.images) > 1 else list(all_results.values())[0], args.save)


if __name__ == "__main__":
    main()
