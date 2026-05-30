"""
🚀 REAL-WORLD ASYNCIO PROJECT
Download 12 Images with Speed Tracking & Image Processing

Features:
- Download 12 images concurrently
- Track download speed per image
- Process images (resize, convert)
- Calculate processing speed
- Generate performance report
"""

import asyncio
import aiohttp
import os
import time
from pathlib import Path
from PIL import Image
from io import BytesIO
import json
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

# 12 Random image URLs
IMAGE_URLS = [
    "https://picsum.photos/800/600?random=1",
    "https://picsum.photos/800/600?random=2",
    "https://picsum.photos/800/600?random=3",
    "https://picsum.photos/800/600?random=4",
    "https://picsum.photos/800/600?random=5",
    "https://picsum.photos/800/600?random=6",
    "https://picsum.photos/800/600?random=7",
    "https://picsum.photos/800/600?random=8",
    "https://picsum.photos/800/600?random=9",
    "https://picsum.photos/800/600?random=10",
    "https://picsum.photos/800/600?random=11",
    "https://picsum.photos/800/600?random=12",
]

# Folders
DOWNLOAD_FOLDER = "downloaded_images"
PROCESSED_FOLDER = "processed_images"

# Create folders if don't exist
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)
Path(PROCESSED_FOLDER).mkdir(exist_ok=True)

# ============================================================================
# DATA STRUCTURES FOR TRACKING
# ============================================================================

class ImageMetadata:
    """Store image download and processing info"""
    def __init__(self, url, index):
        self.url = url
        self.index = index
        self.filename = f"image_{index:02d}.jpg"
        
        # Download metrics
        self.download_start_time = None
        self.download_end_time = None
        self.download_time = None
        self.file_size = None
        self.download_speed = None  # KB/s
        self.download_status = "pending"
        
        # Processing metrics
        self.process_start_time = None
        self.process_end_time = None
        self.process_time = None
        self.process_status = "pending"
        self.original_size = None
        self.processed_size = None
        
        # Error handling
        self.error = None
    
    def to_dict(self):
        return {
            "index": self.index,
            "filename": self.filename,
            "download_time_sec": round(self.download_time, 3) if self.download_time else None,
            "download_speed_kbps": round(self.download_speed, 2) if self.download_speed else None,
            "file_size_kb": round(self.file_size / 1024, 2) if self.file_size else None,
            "process_time_sec": round(self.process_time, 3) if self.process_time else None,
            "original_size_kb": round(self.original_size / 1024, 2) if self.original_size else None,
            "processed_size_kb": round(self.processed_size / 1024, 2) if self.processed_size else None,
            "download_status": self.download_status,
            "process_status": self.process_status,
            "error": self.error
        }


# ============================================================================
# DOWNLOAD IMAGES
# ============================================================================

async def download_image(session, image_meta):
    """
    Download single image and track speed
    
    Args:
        session: aiohttp ClientSession
        image_meta: ImageMetadata object
    """
    try:
        print(f"⬇️  Downloading image {image_meta.index}...")
        image_meta.download_start_time = time.time()
        
        async with session.get(image_meta.url, timeout=30) as response:
            if response.status == 200:
                # Read image data
                image_data = await response.read()
                image_meta.file_size = len(image_data)
                
                # Save to file
                file_path = os.path.join(DOWNLOAD_FOLDER, image_meta.filename)
                with open(file_path, 'wb') as f:
                    f.write(image_data)
                
                # Calculate metrics
                image_meta.download_end_time = time.time()
                image_meta.download_time = image_meta.download_end_time - image_meta.download_start_time
                
                # Speed in KB/s
                image_meta.download_speed = (image_meta.file_size / 1024) / image_meta.download_time
                image_meta.download_status = "success"
                
                print(f"✅ Image {image_meta.index} downloaded in {image_meta.download_time:.3f}s @ {image_meta.download_speed:.2f} KB/s")
                
                return image_meta
            else:
                image_meta.error = f"HTTP {response.status}"
                image_meta.download_status = "failed"
                print(f"❌ Failed to download image {image_meta.index}: HTTP {response.status}")
                return image_meta
    
    except asyncio.TimeoutError:
        image_meta.error = "Timeout"
        image_meta.download_status = "failed"
        print(f"❌ Timeout downloading image {image_meta.index}")
        return image_meta
    
    except Exception as e:
        image_meta.error = str(e)
        image_meta.download_status = "failed"
        print(f"❌ Error downloading image {image_meta.index}: {str(e)}")
        return image_meta


async def download_all_images():
    """Download all 12 images concurrently"""
    print("\n" + "="*60)
    print("🔄 STARTING IMAGE DOWNLOADS")
    print("="*60 + "\n")
    
    # Create metadata for all images
    image_metadata_list = [
        ImageMetadata(url, i+1) 
        for i, url in enumerate(IMAGE_URLS)
    ]
    
    # Download concurrently
    async with aiohttp.ClientSession() as session:
        tasks = [
            download_image(session, meta) 
            for meta in image_metadata_list
        ]
        results = await asyncio.gather(*tasks)
    
    return results


# ============================================================================
# PROCESS IMAGES
# ============================================================================

async def process_image(image_meta):
    """
    Process image asynchronously
    - Resize to 400x300
    - Convert to RGB
    - Reduce quality
    
    Args:
        image_meta: ImageMetadata object
    """
    try:
        if image_meta.download_status != "success":
            image_meta.process_status = "skipped"
            return image_meta
        
        print(f"🔧 Processing image {image_meta.index}...")
        image_meta.process_start_time = time.time()
        
        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        
        file_path = os.path.join(DOWNLOAD_FOLDER, image_meta.filename)
        
        # Get original file size
        image_meta.original_size = os.path.getsize(file_path)
        
        def process_sync():
            # Open image
            with Image.open(file_path) as img:
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize image
                img.thumbnail((400, 300), Image.Resampling.LANCZOS)
                
                # Save processed image
                output_path = os.path.join(PROCESSED_FOLDER, image_meta.filename)
                img.save(output_path, quality=85, optimize=True)
                
                # Get processed file size
                processed_size = os.path.getsize(output_path)
                
                return processed_size
        
        # Run blocking operation in executor
        image_meta.processed_size = await loop.run_in_executor(None, process_sync)
        
        # Calculate metrics
        image_meta.process_end_time = time.time()
        image_meta.process_time = image_meta.process_end_time - image_meta.process_start_time
        image_meta.process_status = "success"
        
        # Calculate compression ratio
        compression = ((image_meta.original_size - image_meta.processed_size) / image_meta.original_size) * 100
        
        print(f"✅ Image {image_meta.index} processed in {image_meta.process_time:.3f}s (Compression: {compression:.1f}%)")
        
        return image_meta
    
    except Exception as e:
        image_meta.error = f"Processing: {str(e)}"
        image_meta.process_status = "failed"
        print(f"❌ Error processing image {image_meta.index}: {str(e)}")
        return image_meta


async def process_all_images(image_metadata_list):
    """Process all images concurrently"""
    print("\n" + "="*60)
    print("🔄 STARTING IMAGE PROCESSING")
    print("="*60 + "\n")
    
    tasks = [
        process_image(meta) 
        for meta in image_metadata_list
    ]
    results = await asyncio.gather(*tasks)
    
    return results


# ============================================================================
# PERFORMANCE ANALYSIS
# ============================================================================

def generate_report(image_metadata_list):
    """Generate performance report"""
    print("\n" + "="*60)
    print("📊 PERFORMANCE REPORT")
    print("="*60 + "\n")
    
    # Download Statistics
    successful_downloads = len([m for m in image_metadata_list if m.download_status == "success"])
    failed_downloads = len([m for m in image_metadata_list if m.download_status == "failed"])
    
    download_times = [m.download_time for m in image_metadata_list if m.download_time]
    download_speeds = [m.download_speed for m in image_metadata_list if m.download_speed]
    total_download_size = sum([m.file_size for m in image_metadata_list if m.file_size]) / 1024  # KB
    total_download_time = sum(download_times)
    
    # Processing Statistics
    successful_processing = len([m for m in image_metadata_list if m.process_status == "success"])
    failed_processing = len([m for m in image_metadata_list if m.process_status == "failed"])
    
    process_times = [m.process_time for m in image_metadata_list if m.process_time]
    total_process_time = sum(process_times)
    total_original_size = sum([m.original_size for m in image_metadata_list if m.original_size]) / 1024  # KB
    total_processed_size = sum([m.processed_size for m in image_metadata_list if m.processed_size]) / 1024  # KB
    
    # Print Report
    print("📥 DOWNLOAD STATISTICS")
    print("-" * 60)
    print(f"Total Images: {len(image_metadata_list)}")
    print(f"Successful: {successful_downloads} ✅")
    print(f"Failed: {failed_downloads} ❌")
    print(f"Total Downloaded: {total_download_size:.2f} KB")
    print(f"Total Download Time: {total_download_time:.3f} seconds")
    print(f"Average Download Speed: {sum(download_speeds)/len(download_speeds):.2f} KB/s" if download_speeds else "N/A")
    print(f"Fastest Download: {max(download_speeds):.2f} KB/s" if download_speeds else "N/A")
    print(f"Slowest Download: {min(download_speeds):.2f} KB/s" if download_speeds else "N/A")
    
    print("\n🔧 PROCESSING STATISTICS")
    print("-" * 60)
    print(f"Successful: {successful_processing} ✅")
    print(f"Failed/Skipped: {failed_processing} ❌")
    print(f"Original Size: {total_original_size:.2f} KB")
    print(f"Processed Size: {total_processed_size:.2f} KB")
    print(f"Total Compression: {((total_original_size - total_processed_size)/total_original_size)*100:.1f}%")
    print(f"Total Processing Time: {total_process_time:.3f} seconds")
    print(f"Average Processing Time per Image: {total_process_time/successful_processing:.3f} seconds" if successful_processing else "N/A")
    
    print("\n⏱️  OVERALL PERFORMANCE")
    print("-" * 60)
    total_time = total_download_time + total_process_time
    print(f"Total Execution Time: {total_time:.3f} seconds")
    print(f"Images per Second: {len(image_metadata_list)/total_time:.2f}" if total_time > 0 else "N/A")
    
    # Detailed breakdown
    print("\n📋 DETAILED BREAKDOWN (Per Image)")
    print("-" * 60)
    print(f"{'Img':<4} {'DL Time':<10} {'DL Speed':<12} {'Proc Time':<12} {'Status':<20}")
    print("-" * 60)
    
    for meta in image_metadata_list:
        dl_time = f"{meta.download_time:.3f}s" if meta.download_time else "N/A"
        dl_speed = f"{meta.download_speed:.2f}KB/s" if meta.download_speed else "N/A"
        proc_time = f"{meta.process_time:.3f}s" if meta.process_time else "N/A"
        status = f"{meta.download_status}/{meta.process_status}"
        
        print(f"{meta.index:<4} {dl_time:<10} {dl_speed:<12} {proc_time:<12} {status:<20}")
    
    return {
        "download": {
            "total_images": len(image_metadata_list),
            "successful": successful_downloads,
            "failed": failed_downloads,
            "total_size_kb": round(total_download_size, 2),
            "total_time_sec": round(total_download_time, 3),
            "avg_speed_kbps": round(sum(download_speeds)/len(download_speeds), 2) if download_speeds else None,
        },
        "processing": {
            "successful": successful_processing,
            "failed": failed_processing,
            "total_time_sec": round(total_process_time, 3),
            "avg_time_per_image": round(total_process_time/successful_processing, 3) if successful_processing else None,
            "original_size_kb": round(total_original_size, 2),
            "processed_size_kb": round(total_processed_size, 2),
            "compression_percent": round(((total_original_size - total_processed_size)/total_original_size)*100, 2),
        },
        "overall": {
            "total_time_sec": round(total_time, 3),
            "images_per_second": round(len(image_metadata_list)/total_time, 2) if total_time > 0 else None,
        }
    }


def save_report_to_json(image_metadata_list, stats):
    """Save detailed report to JSON file"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": stats,
        "detailed": [meta.to_dict() for meta in image_metadata_list]
    }
    
    with open("download_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("\n💾 Report saved to: download_report.json")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Main execution flow"""
    try:
        # Step 1: Download all images
        downloaded_images = await download_all_images()
        
        # Step 2: Process all images
        processed_images = await process_all_images(downloaded_images)
        
        # Step 3: Generate report
        stats = generate_report(processed_images)
        
        # Step 4: Save to JSON
        save_report_to_json(processed_images, stats)
        
        print("\n" + "="*60)
        print("✨ All tasks completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Fatal Error: {str(e)}")


if __name__ == "__main__":
    # Run async main function
    asyncio.run(main())