# Pac-Man

Este é um projeto de recriação do clássico jogo Pac-Man. O objetivo é navegar pelo labirinto, coletar todos os pontos e evitar os fantasmas.

## Como Jogar

O objetivo principal é acumular a maior pontuação possível comendo todos os pontos espalhados pelo labirinto sem ser capturado pelos fantasmas.

### Mecânicas Principais

* **Pontos (Pac-Dots):** Itens comuns que aumentam a pontuação. O nível termina quando todos são coletados.
* **Pastilhas de Força (Power Pellets):** Itens maiores situados nos cantos do mapa. Ao comê-los, os fantasmas ficam vulneráveis temporariamente (ficam azuis) e podem ser comidos pelo Pac-Man para pontos extras.

### Controles

* **Seta para Cima:** Move o Pac-Man para cima.
* **Seta para Baixo:** Move o Pac-Man para baixo.
* **Seta para Esquerda:** Move o Pac-Man para a esquerda.
* **Seta para Direita:** Move o Pac-Man para a direita.

## Os Fantasmas

Cada fantasma possui uma "personalidade" e um algoritmo de perseguição distinto, tornando o jogo estratégico:

1.  **Blinky (Vermelho):**
    * É o perseguidor direto.
    * Ele persegue o Pac-Man incansavelmente, mirando diretamente na posição atual do jogador.
    * Geralmente é o fantasma mais agressivo.

2.  **Pinky (Rosa):**
    * É o emboscador.
    * Ele tenta prever o movimento do jogador, mirando em uma posição à frente de onde o Pac-Man está indo.
    * O objetivo dele é cercar o jogador, não apenas segui-lo.

3.  **Inky (Ciano):**
    * É o estrategista imprevisível.
    * A posição alvo dele é calculada com base na posição do Pac-Man e na posição do Blinky.
    * Isso faz com que seus movimentos pareçam erráticos, ora cercando o jogador, ora perseguindo diretamente.

4.  **Clyde (Laranja):**
    * É o "covarde" ou indeciso.
    * Se ele estiver longe do Pac-Man, ele persegue como o Blinky.
    * Se ele chegar muito perto do Pac-Man (menos de 8 blocos de distância), ele desiste da perseguição e foge para o canto inferior esquerdo do labirinto.