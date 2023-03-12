# FlaskAPIProjectTemplate
这个是知识图谱组建立FlaskAPI项目的模板

```
project_root            整个代码项目的根目录
│   README.md           对于整个项目的介绍
│   .gitignore          对于某些文件和目录让Git忽略管理
│   requirements.txt    声明整个项目依赖的Python库
│   definitions.py      对于整个项目级别的一些常量进行定义，方便其他地方引用。默认有一个ROOT_DIR的常量是项目根目录。
│                       在代码中千万不要使用绝对路径，要使用基于ROOT_DIR的相对路径。
|
└───app                 这是整个项目的核心代码的目录，一般就用项目名。
│   │   __init__.py     蓝图注册
│   └───module1         独立的功能模块接口
│   │   │   views.py    当前模块的视图，蓝图创建及路由配置
│   │   │   models.py   当前模块的模型数据
│   │   │   ...
│   └───module2         独立的功能模块接口
│       │   views.py    当前模块的视图，蓝图创建及路由配置
│       │   models.py   当前模块的模型数据
│       │   ...
│
└───data                存放项目依赖的数据的目录
│
└───doc                 存放项目相关的文档
│
└───output              存放项目的输出，里面内容一般不进行Git托管，都是保留在本地的
│
└───script              这是目录底下存放一些执行脚本，一般是非常特定的。要和可复用的项目代码区别开来。
│
└───test                测试包，里面是与核心模块一一对应的测试文件，目录结构保持一致
```

# 项目的README.md的模板
来源[Github](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)

# Project Title

One Paragraph of project description goes here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
