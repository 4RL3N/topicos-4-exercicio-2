# Análise SIM 2024 - Visualização Interativa

Este projeto é uma aplicação em Python com interface gráfica (Tkinter) que permite a visualização de análises da base de dados SIM 2024. Através de gráficos interativos, o usuário pode explorar informações sobre causas de óbitos, distribuição por sexo, assistência médica recebida e propostas de estudos com base nos dados.

---

## Funcionalidades

- **Questão 1:** Distribuição do campo `ASSISTMED` (assistência médica durante a doença).  
- **Questão 2:** Top 5 causas básicas de óbito (`CAUSABAS`).  
- **Questão 3:** Distribuição das classes após balanceamento (upsampling das causas minoritárias).  
- **Questão 4:** Distribuição por sexo de óbitos com causa `C500` (câncer de mama).  
- **Questão 5:** Proposta de estudo detalhada sobre mortalidade materna e neonatal.

---

## Dependências

O projeto utiliza as seguintes bibliotecas Python:

- `pandas`  
- `matplotlib`  
- `seaborn`  
- `scikit-learn` (para upsampling)  
- `tkinter` (já incluído na instalação padrão do Python)

---

## Instalação com `requirements.txt`

Crie um arquivo chamado `requirements.txt` na mesma pasta do projeto com o seguinte conteúdo:

pandas
matplotlib
seaborn
scikit-learn

Depois, execute o comando abaixo para instalar todas as dependências de uma só vez:

`pip install -r requirements.txt`

---

### Como executar

Certifique-se de ter o arquivo SIM2024.csv na mesma pasta do script Python. O mesmo pode ser baixado [nesse link](https://drive.google.com/file/d/1CD-v127jM66qooATE1nMgLVoZD2_Xnn7/view).


Abra o terminal ou prompt de comando e navegue até a pasta do projeto.

Execute o script principal:

`- python main.py`

A interface gráfica será aberta, permitindo selecionar cada gráfico ou proposta de estudo.

---

## Observações

- Cada gráfico abre em uma janela própria, com informações detalhadas e texto explicativo.

- O scroll está habilitado para gráficos e textos maiores, permitindo fácil visualização de todos os dados.

- Para sair da aplicação, basta clicar no botão Sair na janela principal.

---

## Licença

Este projeto é destinado a fins acadêmicos e educativos.

---

## Autor

Arlen Ferreira da Silva Filho
Centro de Informática - UFPE
