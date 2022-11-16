import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="Memory64",
  version="1.0.3dev2",
  author="忆梦",
  author_email="2872930558@qq.com",
  description="一个内存读写模块, 今后会更加的完善, 在此非常感谢大家的支持 !",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://space.bilibili.com/84500837",
  packages=setuptools.find_packages(),
  include_package_data=True,
)
