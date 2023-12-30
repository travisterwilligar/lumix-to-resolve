# lumix-to-resolve
Lumix to Davinci Resolve Meta Data import tool

## Script to do
* cleanly handle no input files

### to do
* what it does
    * I extracts basic meta data from lumix video files such as aperture, iso, etc and encodes that metadata into a format davinci resolve can import.
* dependencies
    * exif tool
    * python 3
    * Mac and windows installer
    * xmltodict - how to install (optional, but recommended)
* how to install the script
    * sudo cp getmetadata.py /usr/local/bin
    * sudo chmod +x getmetadata.py
* running the script
    * go into the folder containing your videos and type getmetadata.py
* importing metadata into resolve

