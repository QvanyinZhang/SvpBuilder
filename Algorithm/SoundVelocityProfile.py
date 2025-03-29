from datetime import datetime
from typing import List
import numpy as np
import xarray as xr
from pathlib import Path
from .SoundSpeedSea import sound_speed_sea_coppens


class SoundVelocityProfile:
    def __init__(self):
        self.name = ""
        self.time = datetime.now()
        self.time_qc = False
        self.latitude = 0.0
        self.longitude = 0.0
        self.position_qc = False
        self.pressure = np.array([])
        self.pres_qc = False
        self.temperature = np.array([])
        self.temp_qc = False
        self.salinity = np.array([])
        self.sali_qc = False
        self.depth = np.array([])
        self.dep_qc = False
        self.speed = np.array([])
        self.speed_qc = False
        self.status = 0


    def fromDatasetAt(self, dataset, index):
        if not all(name in dataset.variables for name in ['TIME','LATITUDE','LONGITUDE','PRES_ADJUSTED'] ):
            print("Key variables are missing")
            return

        self.name = Path(dataset.encoding['source']).stem + '-' + str(index)

        num_svp = dataset.sizes['TIME']
        if index >= num_svp:
            print("index 超出 dataset.sizes['TIME']")
            return

        self.name = Path(dataset.encoding['source']).stem
        if num_svp > 1:
            self.name = self.name + '(' + str(index) + ')'

        self.time = dataset['TIME'].data[index]
        self.time_qc = dataset['TIME_QC'].data[index] > 0
        self.latitude = dataset['LATITUDE'].data[index]
        self.longitude = dataset['LONGITUDE'].data[index]
        self.position_qc = dataset['POSITION_QC'].data[index] > 0
        self.pressure = dataset['PRES_ADJUSTED'].data[index,:]
        self.pres_qc = dataset['PRES_ADJUSTED_QC'].data[index] > 0

        if 'TEMP_ADJUSTED' in dataset.variables:
            self.temperature = dataset['TEMP_ADJUSTED'].data[index, :]
            self.temp_qc = dataset['TEMP_ADJUSTED_QC'].data[index] > 0

        if 'PSAL_ADJUSTED' in dataset.variables:
            self.salinity = dataset['PSAL_ADJUSTED'].data[index,:]
            self.sali_qc = dataset['PSAL_ADJUSTED_QC'].data[index] > 0


    def preprocess(self, model='coppens'):
        self.depth = self.pressure
        self.dep_qc = self.pres_qc
        if self.temperature.size != self.salinity.size or self.salinity.size != self.depth.size:
            return
        if self.temperature.size == 0 or self.salinity.size == 0 or self.depth.size == 0:
            return

        self.speed_qc = np.logical_and.reduce([self.temp_qc, self.sali_qc, self.dep_qc])
        if model == 'coppens':
            self.speed = sound_speed_sea_coppens(self.temperature, self.salinity, self.depth)
            self.status = 1