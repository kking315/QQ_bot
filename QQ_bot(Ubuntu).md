## 安装[QQ](https://im.qq.com/linuxqq/index.shtml)

QQ Linux版 目前支持x64（x86_64、amd64）、arm64（aarch64）、mips64（mips64el）三种架构，每种架构支持Debian系、红帽系、Arch Linux系、其它发行版中的一种或几种（未来可能继续扩充）。每一次发布均会提供架构和发行版的若干种组合支持的安装包，可按下面所述的规则进行选择。

每一个安装包会按照形如如下的格式命名：

![image-20241030201358721](https://github.com/user-attachments/assets/7a94d487-57cb-45fd-8b48-b640919b584a)


### 1、选择架构：

根据你所使用的机器硬件架构选择相应的兼容架构类型（可通过uname -a查看）x64（x86_64、amd64）、arm64（aarch64）、mips64（mips64el）

### 2、根据你所使用的linux发行版选择格式：

| 后缀名      | 安装包管理器 | 支持发行版                             |
| ----------- | ------------ | -------------------------------------- |
| .rpm        | rpm/yum      | 红帽系（如redhat、fedora、centos）     |
| .deb        | dpkg/apt     | debian系（如debian、ubuntu、银河麒麟） |
| .pkg.tar.xz | pacman       | arch系（如Arch Linux、manjaro）        |
| .sh         | bash         | 任意支持bash的发行版                   |

### 如何安装？

当前版本的QQ Linux版依赖gtk2.0，安装QQ Linux版前请确保你的系统已安装gtk2.0。以下是一些使用命令行安装gtk2.0的例子：

```shell
sudo apt install libgtk2.0-0 # Ubuntu
sudo yum install gtk2.x86_64 # centos
```

请参考你所使用的系统安装包管理器的使用说明来安装你所选择的QQ Linux版安装程序，注意你需要root权限才能完成安装。在一些发行版中你可以通过双击文件管理器中的安装程序完成安装。以下是一些使用命令行来安装的例子：

```shell
sudo ./linuxqq_1.0.1-b1-100_x86_64.sh
sudo rpm -ivh linuxqq_1.0.1-b1-100_mips64el.rpm
sudo dpkg -i linuxqq_1.0.1-b1-100_armhf.deb
sudo apt install -y /path/to/linuxqq_1.0.1-b1-100_amd64.deb
sudo pacman -U linuxqq_1.0.1-ci-94_x86_64.pkg.tar.xz
```

如果版本更新后登录出现闪退情况，请删除 ~/.config/tencent-qq/#你的QQ号# 

目录后重新登录。

### 如何卸载？

请尽量使用你安装时使用的对应方式来卸载QQ Linux版（参考你所使用的系统安装包管理器说明）。同样需要root权限才能完成卸载。以下是一些例子：

```shell
sudo rpm -e linuxqq
sudo dpkg -r linuxqq
```

### 安装示例(Ubuntu 22.04)：

1、官网下载最新版LinuxQQ安装包

![11111111111111111](https://github.com/user-attachments/assets/8b8c059a-8faa-4107-ac9d-c47dd06e7781)


2、安装依赖

```shell
sudo apt install libgtk2.0-0
```

3、安装

一般下载到Downloads文件夹下，所以先打开文件夹

```shell
cd Downloads
sudo dpkg -i QQ_3.2.13_241023_amd64_01.deb
```

