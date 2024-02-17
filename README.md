# 配置环境
```bash
python3 -m venv env
```

# 激活环境

```bash
source env/bin/activate
```


# 安装包
```bash
pip install fastapi
pip install "uvicorn[standard]"
pip install requests
```


# 启动程序
```bash
uvicorn main:app --host 0.0.0.0 --port 8899 --reload
```

# 后台运行
> 挂在后台用tmux
```bash
sudo apt install tmux

tmux new -s download

uvicorn main:app --host 0.0.0.0 --port 8899 --reload
```
<kbd>ctrl</kbd> + <kbd>b</kbd> + <kbd>d</kbd>