@echo off
echo 正在创建虚拟环境...
python -m venv venv

echo 激活虚拟环境...
call venv\Scripts\activate.bat

echo 安装依赖...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo 安装游戏...
python setup.py install

echo 安装完成！
echo 运行 'snake-game' 开始游戏
pause 