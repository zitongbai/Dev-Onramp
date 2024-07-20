# Dev-Onramp
本项目旨在通过完成一个机械臂视觉抓取工作，使得初学者熟悉基本的开发工具与流程

# 预备知识与技能

## 1. 编程语言

- Python

请自己学习Python的基本语法，了解基本的编程思想。至少学到并学完面向对象编程的部分。

## 2. 控制理论

简单了解一下控制理论的基本概念、思路。推荐学习资料：

- [自动控制原理](https://www.bilibili.com/video/BV1jt411M7QU/?spm_id_from=333.999.0.0&vd_source=1044f06951d7c09679a69f0da30419f1)

简单了解反馈控制的思想即可。

## 3. 计算机视觉

简单了解一下计算机视觉的基本知识。

网上有很多教程，可以自行搜索。


# 环境配置

为方便初学者学习，这里仅用Python作为开发语言。对操作系统不做要求，Windows、Linux均可使用。

## 1. Python环境安装

为了方便环境管理，可以使用Anaconda或Miniconda来安装Python环境。推荐使用Miniforge，它是一个基于conda的Python环境管理工具。

这里先解释一下为什么什么时Python环境：对于开发人员而言，不同的项目可能需要不同的Python环境，因为不同的项目可能需要不同的Python版本或者不同的Python库。为了方便管理这些环境，我们使用conda来管理Python环境。这些环境被称为conda环境，它们之间是相互独立的。

安装Miniforge的方法为：从Miniforge的github仓库下载Miniforge的安装包：[Miniforge](https://github.com/conda-forge/miniforge#miniforge3)下载相应操作系统的安装包并安装。

安装完成后，打开命令行（windows中需要打开miniforge prompt），输入以下命令：

```shell
conda create -n myenv python=3.10
```

这样就创建了一个名为myenv的conda环境，并且指定了Python的版本为3.10。这里的myenv可以自己取名。

激活这个环境：

```shell
conda activate myenv
```

重要的事情说三遍：

**在开始安装以下每一个库之前，确保激活了上面创建的conda环境！**

**在开始安装以下每一个库之前，确保激活了上面创建的conda环境！**

**在开始安装以下每一个库之前，确保激活了上面创建的conda环境！**

## 2. 安装Mujoco

Mujoco是Google DeepMind的一个仿真引擎，我们将使用它来仿真机械臂的运动。它提供了Python的接口，我们可以通过Python来控制仿真环境中的机械臂。

在刚才已经激活的conda环境中，输入以下命令：

```shell
(myenv) $ pip install mujoco dm_control robot_descriptions
```

这样就安装了Mujoco、dm_control和robot_descriptions三个库。其中dm_control提供了mujoco的一些拓展功能，robot_descriptions则被用于从[mujoco_menagerie](https://github.com/google-deepmind/mujoco_menagerie)中下载模型

输入以下命令来测试Mujoco是否安装成功：

```shell
(myenv) $ python -m mujoco.viewer
```

若弹出一个窗口，说明Mujoco安装成功。

相关连接：
- [Mujoco文档](https://mujoco.readthedocs.io/en/stable/python.html)
- [Mujoco GitHub](https://github.com/google-deepmind/mujoco)
- [dm_control](https://github.com/google-deepmind/dm_control)
- [Mujoco 提供的一些机器人模型](https://github.com/google-deepmind/mujoco_menagerie)


## 3. 安装Pytorch

根据你使用的操作系统，选择合适的安装方式：[Pytorch官网](https://pytorch.org/)。如果电脑上有GPU，推荐安装GPU版本的Pytorch。

例如，在一个有GPU的Linux系统上，可以使用以下命令安装Pytorch：

```shell
(myenv) $ pip3 install torch torchvision torchaudio
```

安装完成之后，检测一下是否安装成功：

```shell
(myenv) $ python -c "import torch; print(torch.__version__)"
```

若输出Pytorch的版本号（例如`2.3.1+cu121`），则安装成功。

## 4. 安装Yolov8

Yolov8是一个目标检测模型，我们将使用它来检测机械臂的目标物体。直接使用以下命令安装：

```shell
(myenv) $ pip install ultralytics
```

安装完成之后，检测一下是否安装成功：

```shell
(myenv) $ python -c "import ultralytics; ultralytics.checks()"
```

例如在一台有GPU的Linux系统上，输出如下：

```shell
Ultralytics YOLOv8.2.60 🚀 Python-3.10.14 torch-2.3.1+cu121 CUDA:0 (NVIDIA GeForce RTX 4060 Laptop GPU, 7915MiB)
Setup complete ✅ (20 CPUs, 15.4 GB RAM, 121.1/230.0 GB disk)
```

相关连接：
- [Yolov8 GitHub](https://github.com/ultralytics/ultralytics)
- [Ultralytics YOLO Docs](https://docs.ultralytics.com/)

## 5. 安装Vscode

注意，我们要安装的是Vscode（Visual Studio Code），而不是Visual Studio。请直接从[官网](https://code.visualstudio.com/)下载并安装。

安装完成后，在Vscode的扩展商店中搜索并安装以下插件：

- Python Extension Pack
- Jupyter

## 6. 安装Git

在windows上，可以直接从[Git官网](https://git-scm.com/download/win)下载并安装。

在Linux上，可以直接使用包管理器安装：

```shell
sudo apt update
sudo apt install git
```



# 开始学习吧！

## 1. 搭建场景

首先，将本项目克隆到本地：

```shell
git clone https://github.com/zitongbai/Dev-Onramp.git
```

然后，在`Dev-Onramp`目录下打开命令行终端，或者在命令行终端打开到`Dev-Onramp`目录。

激活conda环境：

```shell
conda activate myenv
```

在命令行中执行以下命令，创建一个mujoco场景：

```shell
(myenv) $ python setup_scene.py
```

提示：
- 在vsocde中，可以使用Ctrl+`（键盘上esc下面那个建）打开命令行终端

这个命令会在当前目录下生成一个名为`ur5e_with_robotiq_2f85`的文件夹，里面包含了一个机械臂的模型与Mujoco的场景。

运行如下命令，检测场景是否设置成功：

```shell
(myenv) $ python test_scene.py
```

如果成功，你将会看到两个弹出的窗口，一个是Mujoco的仿真窗口，包含一个机械臂的模型；另一个是机械臂末端执行器上相机的视角图像。

## 2. 各个部分的学习

在`Dev-Onramp`目录下，有若干个Jupyter Notebook文件。请用vscode打开它们并按照顺序学习。

- Task 1: 仿真的基本概念与方法
