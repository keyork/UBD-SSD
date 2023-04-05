# ubd-ssd

THU UAV Ball Detector based on SSD

清华大学无人机比赛，足球篮球排球检测

## Envs

```
torch==1.3.0
numpy
opencv-python
```

用 pip 和 conda 都可

## Usage

下载好权重文件，放在`./weights_ours/`下（如果没有这个文件夹就自己手动创建一下）

在运行无人机程序(tello-control)之前，到这个目录下运行

```
python run_detector.py
```

会自动从`../temp.jpg`读取图像，并将结果（一个字符，足篮排的首字母(f,b,v)）写入`../temp.txt`，如果没检测到就写入`e`

不过这里好像还有点小 bug，一会修一下

## Bugs

- [x] 检测为空的处理
- [ ] torch>=1.3.0 对于 static forward method 的修改，现在会有很多 warning
