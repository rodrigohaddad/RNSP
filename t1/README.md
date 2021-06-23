### Objetivo
Este trabalho tem como objetivo aplicar uma Rede Neural Sem Peso (RNSP) ao dataset Kuzushiji-MNIST. A RNSP será utilizada através da biblioteca WiSARDPKG. O dataset KMNIST é composto por 70000 imagens de dimensões 28x28 em escala de cinza. Cada classe de caractere Kuzushiji é rotulado por um caractere do alfabeto latino, formando um total de 10 classes.

A WiSARDPKG é uma biblioteca que implementa uma rede neural sem peso. Ou seja, ao invés de utilizar sinapses com peso para guardar a informação aprendida pelos padrões observados, possui neurônios baseados em RAM (random-access-memory). Em uma RNSP, a aprendizagem de um padrão corresponde à escrita na memória, enquanto a classificação corresponde a leitura de certas posições dessa memória. [referenciar A library for WiSARD-based models]

### Binarizações
Os métodos de classificação e clusterização da WiSARDPKG aceitam apenas entradas compostas por vetores de números binários. Como os valores dos vetores direto do dataset variam de 0 a 255, é necessário que técnicas de binarização sejam aplicadas. É vasta a quantidade de técnicas de binarização que podem ser aplicadas e, como a binarização escolhida influencia diretamente na acurácia do modelo, foram feitos testes com diferentes algoritmos. 

#### Binarização simples
Aplicação de um "threshold" para mapear valores para 0 e 1. Números abaixo de 127 são mapeados para 0, enquanto números de 128 a 255 são mapeados para 1.

#### Termômetro simples
Esse algoritmo divide a janela de valores possíveis (0 a 255) em n pedaços. Cada pedaço é preenchido por 0 ou 1, de acordo com o valor que a representa. Como o termômetro basicamente transforma um número em um vetor, problemas de performance podem ser encontrados.

#### Termômetro circular

#### Kernel Canvas
#### Sauvola
#### Niblack

### Predições
#### Wisard:
#### ClusWisar:

### Medição de acurácia
#### Score:
#### Imagens mentais:


