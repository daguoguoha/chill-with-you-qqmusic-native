修复 QQ 音乐 v1.0.1 一键安装过程中下载 BepInEx.zip 超时的问题。

下载 **ChillQQMusicNative-1.0.2-OneClick.zip**，完整解压后退出游戏，再双击 **ChillQQMusicSetup.exe**。BepInEx 5.4.23.5 与 NAudio 2.2.1 官方依赖已经内置，安装阶段无需联网下载，仍逐个校验 SHA256。不要只复制安装器，offline-dependencies 文件夹必须保留。

本次只修改安装器和打包，游戏插件沿用已验证的 v1.0.1，F9、原生播放器切歌、隐藏入口均保留。账号与存档不会打包，也不会在更新时清除。登录、歌单和音乐播放仍需联网。

源码、原生桥接对应源码、依赖来源和开源许可证随包提供，详细信息见 README.md 和 THIRD_PARTY_NOTICES.md。
