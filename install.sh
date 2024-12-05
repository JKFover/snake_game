#!/bin/bash

echo "正在创建虚拟环境..."
python3 -m venv venv

echo "激活虚拟环境..."
source venv/bin/activate

echo "安装依赖..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "安装游戏..."
python setup.py install

echo "安装完成！"
echo "运行 'snake-game' 开始游戏" 