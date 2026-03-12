# Sistema de Monitoramento de Silos (IoT)

Sistema desenvolvido para **monitoramento e controle de silos utilizando dispositivos IoT**, permitindo a coleta de dados de sensores e o gerenciamento de atuadores por meio de uma aplicação em Python.

O projeto possui **caráter extensionista**, desenvolvido em parceria com a **Fazenda Gralha Azul da PUCPR**. Durante o projeto foram levantados desafios reais enfrentados pela fazenda relacionados ao **monitoramento de estruturas de armazenamento e dispositivos conectados**, e a partir dessas necessidades foi proposta a criação de um sistema capaz de **organizar dados de sensores, gerenciar dispositivos e estruturar a comunicação entre componentes IoT**.

A aplicação foi desenvolvida utilizando **Python com Flask**, empregando **Jinja2** para renderização de templates e organização da interface. O sistema foi projetado com foco em **modularidade e organização de código**, separando responsabilidades entre camadas de controle e modelos de dados, utilizando uma estrutura inspirada em **arquitetura MVC**.

Para simulação do ambiente IoT foi utilizado o **Wokwi**, permitindo reproduzir o funcionamento de sensores e dispositivos conectados em um protótipo virtual. O repositório inclui também um **arquivo de simulação Wokwi** que possibilita executar o protótipo em tempo real.

---

## 📌 Funcionalidades

- 📡 Monitoramento de **sensores IoT**
- ⚙️ Controle de **atuadores**
- 📊 Gerenciamento de **dados coletados pelos sensores**
- 👤 Gerenciamento de **usuários**
- 🧩 Organização modular utilizando **controllers e models**
- 🔄 Comunicação entre dispositivos e aplicação

---

## 🛠️ Tecnologias Utilizadas

- **Python** – Linguagem principal da aplicação  
- **Flask** – Framework web utilizado para estruturar o backend  
- **Jinja2** – Template engine para renderização de páginas  
- **Wokwi** – Simulação de hardware IoT e sensores  
- **Arquitetura modular (controllers e models)** – Organização da aplicação  
- **Estrutura inspirada em MVC** – Separação entre lógica de controle e modelos de dados  

---

## 📂 Estrutura do Projeto

```
Silos_Final/
│
├── app.py                     # Arquivo principal da aplicação
│
├── controllers/               # Camada de controle da aplicação
│   ├── app_controller.py
│   ├── data_controller.py
│   ├── devices_controller.py
│   ├── kit_controller.py
│   └── user_controller.py
│
├── models/                    # Modelos de dados do sistema
│   ├── db.py
│   ├── users_db.py
│   │
│   └── iot/                   # Componentes relacionados a IoT
│       ├── sensors/
│       ├── actuators/
│       └── commands/
│
└── __pycache__/               # Arquivos compilados do Python
```

> Fora da pasta **Silos_Final** encontra-se também um arquivo de **simulação Wokwi**, utilizado para executar o protótipo IoT em ambiente virtual.


## 💡 Conceitos Aplicados

- Desenvolvimento de aplicações backend em **Python**
- Criação de aplicações web utilizando **Flask**
- Renderização de templates com **Jinja2**
- Organização de software utilizando **arquitetura modular**
- Separação de responsabilidades entre **controllers e models**
- Estruturação de sistemas voltados para **IoT**
- Simulação de hardware utilizando **Wokwi**

---

## 👨‍💻 Desenvolvedores

- **Cecília Lucchesi Mardegan**  
  GitHub: https://github.com/ceciLcchM

- **Christine von Schmalz**  
  GitHub: https://github.com/cvschmalz

- **Erick Maestri de Souza**  
  GitHub: https://github.com/ErickMS18
