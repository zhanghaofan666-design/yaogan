from pathlib import Path

import numpy as np
from osgeo import gdal, osr

gdal.UseExceptions()

# 输出文件
output_file = Path(__file__).parent / "test_output.tif"

# 创建 10×10 的测试数据
data = np.arange(100, dtype=np.float32).reshape(10, 10)

# 创建 GeoTIFF
driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create(
    str(output_file),
    10,                  # 宽度
    10,                  # 高度
    1,                   # 波段数
    gdal.GDT_Float32,
)

# 设置地理范围：左上角经度 110、纬度 30，像元大小 0.01°
dataset.SetGeoTransform((110.0, 0.01, 0.0, 30.0, 0.0, -0.01))

# 设置坐标系为 WGS 84
spatial_ref = osr.SpatialReference()
spatial_ref.ImportFromEPSG(4326)
dataset.SetProjection(spatial_ref.ExportToWkt())

# 写入数据
band = dataset.GetRasterBand(1)
band.WriteArray(data)
band.SetNoDataValue(-9999)
band.FlushCache()

# 关闭文件
dataset = None

# 重新读取并验证
dataset = gdal.Open(str(output_file))
band = dataset.GetRasterBand(1)
read_data = band.ReadAsArray()

print("GDAL 版本：", gdal.VersionInfo("--version"))
print("文件位置：", output_file)
print("影像大小：", dataset.RasterXSize, "×", dataset.RasterYSize)
print("波段数量：", dataset.RasterCount)
print("坐标变换：", dataset.GetGeoTransform())
print("最小值：", read_data.min())
print("最大值：", read_data.max())
print("平均值：", read_data.mean())
print("测试结果：成功")

dataset = None