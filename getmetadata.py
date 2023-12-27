#!/usr/bin/env python3
import json, csv, subprocess

try:
    import xmltodict
    xmltodictFound = True
except ImportError:
    xmltodictFound = False

class Metadata:
    def __init__(self, inputFileName, outputFileName):
        self.cameraMetaData = []
        self.inputFileName = inputFileName
        self.outputFileName = outputFileName
        self.row = []
        self.rawMetaData = []
        self.processedMetaData = []
    def get_exif(self):
        subprocess.Popen("exiftool -j -ext mov -ext mp4 . > " + self.inputFileName, shell=True, stdout=subprocess.PIPE).stdout.read()

    def load_exif(self):
        with open(self.inputFileName) as f:
            self.cameraMetaData = json.load(f)
    
    def xml_to_json(self):
        if('PanasonicSemi-ProMetadataXml' in self.row):
            self.panasonic_xml_metadata = self.row['PanasonicSemi-ProMetadataXml']
            self.panasonic_xml_metadata = xmltodict.parse(self.panasonic_xml_metadata)
            self.row['PanasonicSemi-ProMetadataXml'] = self.panasonic_xml_metadata
            self.row['PanasonicSemi-ProMetadataXml-jpn-JP'] = []
            return self.row

    def process_exif(self):
        for row in self.cameraMetaData:
            self.row = row
            if(xmltodictFound != False):
                self.row = self.xml_to_json()
            self.rawMetaData.append(self.row)
            print('\033[92m' + self.row['FileName'] + '\033[0m')

    def map_to_resolve(self):
        for row in self.rawMetaData:
            if(row['DynamicRangeBoost'] and row['DynamicRangeBoost'] == "On"):
                row['ISO'] = str(row['ISO']) + " DR Boost On"

            #Resolve Mapping
            self.metadata = {
                'File Name':                row['FileName'],
                'ISO':                      row['ISO'],
                'Shutter Speed':            row['ShutterSpeed'],
                'Shutter Type':             'Speed',
                'White Point (Kelvin)':     row['WhiteBalance'],
                'Shot Frame Rate':          row['VideoFrameRate'],
                'Camera Type':              row['Model'], 
                'Lens Type':                row['LensType'],             
                'Camera Aperture':          row.get('Aperture'),
                'Focal Point (mm)':         row['FocalLength'],
                'Camera FPS':               row['VideoFrameRate'],
                'Camera Serial #':          row['SerialNumber'],
                'Camera Firmware':          row['FirmwareVersion'],
                # 'Sample Rate (Khz)':        row['PanasonicSemi-ProMetadataXml']['ClipMain']['ClipContent']['EssenceList']['Audio']['SamplingRate'], 
                # 'Bit Rate':                 row['PanasonicSemi-ProMetadataXml']['ClipMain']['ClipContent']['EssenceList']['Audio']['BitsPerSample'], 
                # 'Gamma Notes':              row['PanasonicSemi-ProMetadataXml']['ClipMain']['UserArea']['AcquisitionMetadata']['CameraUnitMetadata']['Gamma']['CaptureGamma'], 
                # 'Color Space Notes':        row['PanasonicSemi-ProMetadataXml']['ClipMain']['UserArea']['AcquisitionMetadata']['CameraUnitMetadata']['Gamut']['CaptureGamut'], 
                # 'Codec Bitrate':            row['PanasonicSemi-ProMetadataXml']['ClipMain']['ClipContent']['EssenceList']['Video']['Codec']['@BitRate'],
                # 'Camera Manufacturer':      row['PanasonicSemi-ProMetadataXml']['ClipMain']['ClipContent']['ClipMetadata']['Device']['Manufacturer'],
            }
            if(xmltodictFound != False):
                self.metadata_extended = {
                    'Sample Rate (Khz)':        row['PanasonicSemi-ProMetadataXml']['ClipMain']['ClipContent']['EssenceList']['Audio']['SamplingRate'], 
                    'Bit Rate':                 row['PanasonicSemi-ProMetadataXml']['ClipMain']['ClipContent']['EssenceList']['Audio']['BitsPerSample'], 
                    'Gamma Notes':              row['PanasonicSemi-ProMetadataXml']['ClipMain']['UserArea']['AcquisitionMetadata']['CameraUnitMetadata']['Gamma']['CaptureGamma'], 
                    'Color Space Notes':        row['PanasonicSemi-ProMetadataXml']['ClipMain']['UserArea']['AcquisitionMetadata']['CameraUnitMetadata']['Gamut']['CaptureGamut'], 
                    'Codec Bitrate':            row['PanasonicSemi-ProMetadataXml']['ClipMain']['ClipContent']['EssenceList']['Video']['Codec']['@BitRate'],
                    'Camera Manufacturer':      row['PanasonicSemi-ProMetadataXml']['ClipMain']['ClipContent']['ClipMetadata']['Device']['Manufacturer'],
                }
                self.metadata.update(self.metadata_extended)
            self.processedMetaData.append(self.metadata)

    def write_csv(self):
        with open(self.outputFileName,'w') as f:
            w = csv.writer(f)
            w.writerow(self.processedMetaData[0].keys())
            for row in self.processedMetaData:
                w.writerow(row.values())
            print('Import metadata to resolve using ' + self.outputFileName)

def main():
    metadata = Metadata('input-exif2.json', 'resolve-metadata.csv')
    metadata.get_exif()
    metadata.load_exif()
    metadata.process_exif()
    metadata.map_to_resolve()
    metadata.write_csv()

if __name__ == "__main__":
    main()