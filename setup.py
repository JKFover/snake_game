from setuptools import setup, find_packages
import os
import sys
import urllib.request

def download_font():
    font_url = "https://github.com/microsoft/font-files/raw/main/SimHei/SimHei.ttf"
    font_path = os.path.join("src", "assets", "simhei.ttf")
    
    if not os.path.exists(os.path.join("src", "assets")):
        os.makedirs(os.path.join("src", "assets"))
    
    if not os.path.exists(font_path):
        print("下载字体文件...")
        try:
            urllib.request.urlretrieve(font_url, font_path)
            print("字体文件下载完成！")
        except Exception as e:
            print(f"字体下载失败: {e}")
            print("请手动下载字体文件并放置在 src/assets/simhei.ttf")

setup(
    name="snake_game",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.6.1",
    ],
    package_data={
        "src": ["assets/*"],
    },
    entry_points={
        "console_scripts": [
            "snake-game=src.game:main",
        ],
    },
)

if __name__ == "__main__":
    download_font() 