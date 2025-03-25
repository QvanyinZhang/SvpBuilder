
from datetime import datetime
from netCDF4 import Dataset, num2date
import xarray as xr
import numpy as np


class SamplePoint:
    def __init__(self, temperature: float, salinity: float, depth: float, sound_speed: float):
        """
        初始化采样点信息
        :param temperature: 温度 (单位：摄氏度)
        :param salinity: 盐度 (单位：PSU)
        :param depth: 深度 (单位：米)
        :param sound_speed: 声速 (单位：m/s)
        """
        self.temperature = temperature
        self.salinity = salinity
        self.depth = depth
        self.sound_speed = sound_speed

    def __repr__(self):
        return (f"SamplePoint(temperature={self.temperature}, "
                f"salinity={self.salinity}, depth={self.depth}, "
                f"sound_speed={self.sound_speed})")


class SoundSpeedProfile:
    def __init__(self, latitude: float, longitude: float, date_info):
        """
        初始化声速剖面信息
        :param latitude: 纬度
        :param longitude: 经度
        :param date_info: 日期信息，可以是 datetime 对象或者 'YYYY-MM-DD' 格式的字符串
        """
        self.latitude = latitude
        self.longitude = longitude
        if isinstance(date_info, datetime):
            self.date = date_info
        else:
            self.date = datetime.strptime(date_info, "%Y-%m-%d")
        self.sample_points = []

    def add_sample_point(self, temperature: float, salinity: float, depth: float, sound_speed: float):
        """
        添加一个采样点
        """
        point = SamplePoint(temperature, salinity, depth, sound_speed)
        self.sample_points.append(point)


    def __repr__(self):
        date_str = self.date.strftime("%Y-%m-%d")
        return (f"SoundSpeedProfile(latitude={self.latitude}, longitude={self.longitude}, "
                f"date='{date_str}', sample_points={self.sample_points})")


def read_nc_file(nc_file_path: str) -> SoundSpeedProfile:
    """
    读取 netCDF 文件，提取温度、盐度、压力信息，并返回一个声速剖面实例
    文件中应包含变量：temperature, salinity, pressure
    同时通过全局属性或变量获取 latitude, longitude, time 信息

    :param nc_file_path: nc 文件的路径
    :return: SoundSpeedProfile 实例
    """
    # 打开 netCDF 文件
    ds = Dataset(nc_file_path, 'r')

    # 获取位置信息（尝试从全局属性或变量中提取）
    # 如果全局属性中没有，可根据实际文件修改变量名
    try:
        latitude = float(getattr(ds, 'latitude'))
    except AttributeError:
        latitude = float(ds.variables['latitude'][0])

    try:
        longitude = float(getattr(ds, 'longitude'))
    except AttributeError:
        longitude = float(ds.variables['longitude'][0])

    # 获取时间信息（这里假设 nc 文件中有一个名为 time 的变量）
    time_var = ds.variables.get('time', None)
    if time_var is not None:
        # 将 netCDF 时间数值转换为 datetime 对象
        time_units = time_var.units
        time_calendar = getattr(time_var, 'calendar', 'standard')
        date_info = num2date(time_var[0], units=time_units, calendar=time_calendar)
    else:
        # 如果没有时间变量，可使用当前日期作为默认值
        date_info = datetime.now()

    # 创建声速剖面实例
    profile = SoundSpeedProfile(latitude=latitude, longitude=longitude, date_info=date_info)

    # 读取温度、盐度、压力信息
    temperature_data = ds.variables['temperature'][:]
    salinity_data = ds.variables['salinity'][:]
    pressure_data = ds.variables['pressure'][:]

    # 假设这三个变量是一维数组且长度一致
    num_points = len(temperature_data)
    for i in range(num_points):
        T = float(temperature_data[i])
        S = float(salinity_data[i])
        # 这里简单将压力数据作为深度，实际应用中可能需要转换
        depth = float(pressure_data[i])
        c = compute_sound_speed(T, S, depth)
        profile.add_sample_point(T, S, depth, c)

    ds.close()
    return profile


def compute_sound_speed(temperature: float, salinity: float, depth: float) -> float:
    """
    根据温度、盐度和深度计算海水中的声速
    使用 Mackenzie 公式 (1981) 的近似形式：

    c = 1448.96 + 4.591 * T - 0.05304 * T^2 + 0.0002374 * T^3 +
        (1.340 - 0.010 * T) * (S - 35) + 0.0163 * depth

    :param temperature: 温度，单位摄氏度
    :param salinity: 盐度，单位 PSU
    :param depth: 深度，单位 米（这里将压力近似为深度）
    :return: 声速，单位 m/s
    """
    c = (1448.96 +
         4.591 * temperature -
         0.05304 * temperature ** 2 +
         0.0002374 * temperature ** 3 +
         (1.340 - 0.010 * temperature) * (salinity - 35) +
         0.0163 * depth)
    return c

class SeaSoundField:
    def __init__(self):
        """
        初始化 SeaSoundField 实例，包含一个声速剖面的列表
        """
        self.sound_speed_profiles = []

    def add_profile_from_file(self, file_path: str) -> SoundSpeedProfile:
        """
        读取指定的 nc 文件，生成声速剖面实例，并添加到列表中
        :param file_path: nc 文件的路径
        :return: 生成的 SoundSpeedProfile 实例
        """
        profile = read_nc_file(file_path)
        self.sound_speed_profiles.append(profile)
        return profile

    def read_nc_file(self, file_path: str):
        ds = xr.open_dataset(file_path)

        required_vars = ['TEMP', 'PSAL', 'PRES']
        for var in required_vars:
            if var not in ds.variables:
                raise KeyError(f"变量 '{var}' 在文件中不存在。")

        temperature = ds['TEMP']
        salinity = ds['PSAL']
        pressure = ds['PRES']

        # 数据清洗（去除缺失值）
        valid_indices = ~np.isnan(temperature) & ~np.isnan(salinity) & ~np.isnan(pressure)
        temp = temperature[valid_indices]
        salinity = salinity[valid_indices]
        pressure = pressure[valid_indices]



    def __repr__(self):
        return f"SeaSoundField(sound_speed_profiles={self.sound_speed_profiles})"
