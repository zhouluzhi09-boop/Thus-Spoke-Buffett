---
title: "MCP Clients · Hugging Face"
source: "https://huggingface.co/learn/mcp-course/unit1/key-concepts"
author:
published:
created: 2026-05-18
description: "We’re on a journey to advance and democratize artificial intelligence through open source and open science."
tags:
  - "clippings"
---
## MCP Course MCP 课程

[901](https://github.com/huggingface/mcp-course)

0\. Welcome to the MCP Course

1\. Introduction to Model Context Protocol

2\. Use Case: End-to-End MCP Application

3\. Advanced MCP Development: Custom Workflow Servers

3.1. Use Case: Build a Pull Request Agent on the Hub

## Key Concepts and Terminology关键概念和术语

Before diving deeper into the Model Context Protocol, it’s important to understand the key concepts and terminology that form the foundation of MCP. This section will introduce the fundamental ideas that underpin the protocol and provide a common vocabulary for discussing MCP implementations throughout the course.  
在深入探讨模型上下文协议 (MCP) 之前，理解构成 MCP 基础的关键概念和术语至关重要。本节将介绍该协议的基本思想，并为整个课程中讨论 MCP 实现提供一套通用词汇。

MCP is often described as the “USB-C for AI applications.” Just as USB-C provides a standardized physical and logical interface for connecting various peripherals to computing devices, MCP offers a consistent protocol for linking AI models to external capabilities. This standardization benefits the entire ecosystem:  
MCP 常被誉为“人工智能应用领域的 USB-C”。正如 USB-C 为连接各种外围设备和计算设备提供了标准化的物理和逻辑接口一样，MCP 也为将人工智能模型与外部功能连接起来提供了一种一致的协议。这种标准化惠及整个生态系统：

- **users** enjoy simpler and more consistent experiences across AI applications  
	**用户** 在人工智能应用中可以享受更简单、更一致的体验。
- **AI application developers** gain easy integration with a growing ecosystem of tools and data sources  
	**AI 应用开发者** 可以轻松集成到不断增长的工具和数据源生态系统中。
- **tool and data providers** need only create a single implementation that works with multiple AI applications  
	**工具和数据提供商** 只需创建一个可与多个人工智能应用程序兼容的单一实现即可。
- the broader ecosystem benefits from increased interoperability, innovation, and reduced fragmentation  
	更广泛的生态系统将受益于互操作性的提高、创新和碎片化的减少。

## The Integration Problem 积分问题

The **M×N Integration Problem** refers to the challenge of connecting M different AI applications to N different external tools or data sources without a standardized approach.  
**M×N 集成问题** 是指在没有标准化方法的情况下，将 M 个不同的 AI 应用程序连接到 N 个不同的外部工具或数据源的挑战。

### Without MCP (M×N Problem)不考虑 MCP（M×N 问题）

Without a protocol like MCP, developers would need to create M×N custom integrations—one for each possible pairing of an AI application with an external capability.  
如果没有像 MCP 这样的协议，开发人员将需要创建 M×N 个自定义集成——每个 AI 应用程序与外部功能的组合都需要一个集成。

![Without MCP](https://huggingface.co/datasets/mcp-course/images/resolve/main/unit1/1.png)

Each AI application would need to integrate with each tool/data source individually. This is a very complex and expensive process which introduces a lot of friction for developers, and high maintenance costs.  
每个人工智能应用都需要单独与每个工具/数据源集成。这是一个非常复杂且成本高昂的过程，会给开发人员带来诸多不便，并增加维护成本。

Once we have multiple models and multiple tools, the number of integrations becomes too large to manage, each with its own unique interface.  
一旦我们有了多个模型和多个工具，集成数量就会变得过于庞大而难以管理，因为每个集成都有其独特的界面。

![Multiple Models and Tools](https://huggingface.co/datasets/mcp-course/images/resolve/main/unit1/1a.png)

### With MCP (M+N Solution)

MCP transforms this into an M+N problem by providing a standard interface: each AI application implements the client side of MCP once, and each tool/data source implements the server side once. This dramatically reduces integration complexity and maintenance burden.

![With MCP](https://huggingface.co/datasets/mcp-course/images/resolve/main/unit1/2.png)

## Core MCP Terminology

Now that we understand the problem that MCP solves, let’s dive into the core terminology and concepts that make up the MCP protocol.

> MCP is a standard like HTTP or USB-C, and is a protocol for connecting AI applications to external tools and data sources. Therefore, using standard terminology is crucial to making the MCP work effectively.
> 
> When documenting our applications and communicating with the community, we should use the following terminology.

### Components

Just like client server relationships in HTTP, MCP has a client and a server.

![MCP Components](https://huggingface.co/datasets/mcp-course/images/resolve/main/unit1/3.png)

- **Host**: The user-facing AI application that end-users interact with directly. Examples include Anthropic’s Claude Desktop, AI-enhanced IDEs like Cursor, inference libraries like Hugging Face Python SDK, or custom applications built in libraries like LangChain or smolagents. Hosts initiate connections to MCP Servers and orchestrate the overall flow between user requests, LLM processing, and external tools.
- **Client**: A component within the host application that manages communication with a specific MCP Server. Each Client maintains a 1:1 connection with a single Server, handling the protocol-level details of MCP communication and acting as an intermediary between the Host’s logic and the external Server.
- **Server**: An external program or service that exposes capabilities (Tools, Resources, Prompts) via the MCP protocol.

> A lot of content uses ‘Client’ and ‘Host’ interchangeably. Technically speaking, the host is the user-facing application, and the client is the component within the host application that manages communication with a specific MCP Server.

### Capabilities

Of course, your application’s value is the sum of the capabilities it offers. So the capabilities are the most important part of your application. MCP’s can connect with any software service, but there are some common capabilities that are used for many AI applications.

| Capability | Description | Example |
| --- | --- | --- |
| **Tools** | Executable functions that the AI model can invoke to perform actions or retrieve computed data. Typically relating to the use case of the application. | A tool for a weather application might be a function that returns the weather in a specific location. |
| **Resources** | Read-only data sources that provide context without significant computation. | A researcher assistant might have a resource for scientific papers. |
| **Prompts** | Pre-defined templates or workflows that guide interactions between users, AI models, and the available capabilities. | A summarization prompt. |
| **Sampling** | Server-initiated requests for the Client/Host to perform LLM interactions, enabling recursive actions where the LLM can review generated content and make further decisions. | A writing application reviewing its own output and decides to refine it further. |

In the following diagram, we can see the collective capabilities applied to a use case for a code agent.

![collective diagram](https://huggingface.co/datasets/mcp-course/images/resolve/main/unit1/8.png)

This application might use their MCP entities in the following way:

| Entity | Name | Description |
| --- | --- | --- |
| Tool | Code Interpreter | A tool that can execute code that the LLM writes. |
| Resource | Documentation | A resource that contains the documentation of the application. |
| Prompt | Code Style | A prompt that guides the LLM to generate code. |
| Sampling | Code Review | A sampling that allows the LLM to review the code and make further decisions. |

### Conclusion

Understanding these key concepts and terminology provides the foundation for working with MCP effectively. In the following sections, we’ll build on this foundation to explore the architectural components, communication protocol, and capabilities that make up the Model Context Protocol.

[Update on GitHub](https://github.com/huggingface/mcp-course/blob/main/units/en/unit1/key-concepts.mdx)

Key Concepts and Terminology