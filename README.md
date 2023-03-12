# Cross-language-tutorial-search
跨语言教程检索 - 推荐系统

```
project_root            
│   README.md           
│   .gitignore          
│   requirements.txt    
│   definitions.py      
│                       
|
└───app                 教程推荐
│   │   __init__.py     
│   └───module1         独立的功能模块接口1
│   │   │   views.py    当前模块的视图，蓝图创建及路由配置
│   │   │   models.py   当前模块的模型数据
│   │   │   ...
│   └───module2         独立的功能模块接口2
│       │   views.py    当前模块的视图，蓝图创建及路由配置
│       │   models.py   当前模块的模型数据
│       │   ...
│
└───data                
│
└───doc                 文档
│
└───output              
│
└───script              
│
└───test                
```



# Cross-language tutorial search

这个项目实现了目前常见的retrieval-rerank架构的检索器，在教程/论坛预料上进行微调。我们构建了相关的训练数据集和知识图谱，并搭建出最终的推荐系统。

This project implements the current common retrieval-rerank architecture for retrievalers, fine-tuning on tutorial/forum expectations. We build the relevant training dataset and knowledge graph, and build the final recommendation system.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
.
.
.
.
.

[//]: # (### Prerequisites)

[//]: # ()
[//]: # (What things you need to install the software and how to install them)

[//]: # ()
[//]: # (```)

[//]: # (Give examples)

[//]: # (```)

[//]: # ()
[//]: # (### Installing)

[//]: # ()
[//]: # (A step by step series of examples that tell you how to get a development env running)

[//]: # ()
[//]: # (Say what the step will be)

[//]: # ()
[//]: # (```)

[//]: # (Give the example)

[//]: # (```)

[//]: # ()
[//]: # (And repeat)

[//]: # ()
[//]: # (```)

[//]: # (until finished)

[//]: # (```)

[//]: # ()
[//]: # (End with an example of getting some data out of the system or using it for a little demo)

[//]: # ()
[//]: # (## Running the tests)

[//]: # ()
[//]: # (Explain how to run the automated tests for this system)

[//]: # ()
[//]: # (### Break down into end to end tests)

[//]: # ()
[//]: # (Explain what these tests test and why)

[//]: # ()
[//]: # (```)

[//]: # (Give an example)

[//]: # (```)

[//]: # ()
[//]: # (### And coding style tests)

[//]: # ()
[//]: # (Explain what these tests test and why)

[//]: # ()
[//]: # (```)

[//]: # (Give an example)

[//]: # (```)

[//]: # ()
[//]: # (## Deployment)

[//]: # ()
[//]: # (Add additional notes about how to deploy this on a live system)

[//]: # ()
[//]: # (## Built With)

[//]: # ()
[//]: # (* [Dropwizard]&#40;http://www.dropwizard.io/1.0.2/docs/&#41; - The web framework used)

[//]: # (* [Maven]&#40;https://maven.apache.org/&#41; - Dependency Management)

[//]: # (* [ROME]&#40;https://rometools.github.io/rome/&#41; - Used to generate RSS Feeds)

[//]: # ()
[//]: # (## Contributing)

[//]: # ()
[//]: # (Please read [CONTRIBUTING.md]&#40;https://gist.github.com/PurpleBooth/b24679402957c63ec426&#41; for details on our code of conduct, and the process for submitting pull requests to us.)

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/hyunsir/Cross-language-tutorial-search/tags).

## Authors

* **Zhang gaoyang** - *Initial work* - [hyunsir](https://github.com/hyunsir)

See also the list of [contributors](https://github.com/hyunsir/Cross-language-tutorial-search/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

[//]: # (* 可爱滴大师兄)

[//]: # (* 敬爱滴教授)
* 知识图谱组滴家人们
* fdu滴小伙伴们
