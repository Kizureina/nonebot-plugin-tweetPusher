# nonebot plugin tweetPusher
![python](https://img.shields.io/pypi/pyversions/nonebot-plugin-picsearcher)
[![license](https://img.shields.io/github/license/synodriver/nonebot_plugin_picsearcher.svg)](https://raw.githubusercontent.com/synodriver/nonebot_plugin_picsearcher/main/LICENSE)
- 基于[nonebot2](https://github.com/nonebot/nonebot2)

## 基本功能
- 推送指定推主的推文

## 快速上手
因为本插件使用了定时任务，需要先添加nonebot2的定时任务插件。

如正在使用 nb-cli 构建项目，你可以从插件市场复制安装命令或手动输入以下命令以添加`nonebot_plugin_apscheduler`

```
nb plugin install nonebot_plugin_apscheduler
```
具体定时任务配置参见[官方文档](https://v2.nonebot.dev/docs/advanced/scheduler).

在 nonebot2 项目的环境文件`.env.*`中添加配置项:
```
TWI_USER=["aaa","bbb"]
PUSHER_USER=["1111111"]
PUSHER_GROUP=["00000000"]
```

