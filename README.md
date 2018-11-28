# Curva-de-Bezier

## Configurações

Para que o algoritmo funcione no seu computador é necessário a instalação do Python3 e do Tkinter (biblioteca do Python3).

Códigos para instalação em sistema Linux:

<code>
  apt-get install python3

  apt-get install python3-tk
</code>

Links que auxiliam ao baixar o Python3 e o Tkinter no Windows:

Python3: https://cadernoscicomp.com.br/instalar-python-3-no-windows/ 
Tkinter: https://tkdocs.com/tutorial/install.html

Para executar o código é necessário digitar a linha de comando: <code> python3 beziercg.py </code>

## Estrutura

O código no arquivo <b>beziercg.py</b> é composto de uma classe chamada <i>CurvaBezier</i>, essa classe contém os componentes de sua respectiva tela, que são um label, dois botões e o canvas, que é a parte da tela destinada ao desenho das aplicações. Essa classe também possui funções que auxiliam no funcionamento da aplicação e funções que são responsáveis pela construção da curva de Bezier. As funções que auxiliam no funcionamento da aplicação são as seguintes:

<ul>
  <li>inicio(): assim que a aplicação se inicia essa função é chamada, ela contém apenas o <i>bind</i> para que quando qualquer parte do canvas seja clicada, a função inicializar_coordenadas(event) seja chamada </li>
  <li>inicio2(): essa função é chamada quando o botão: "Escolher novamente os pontos" é clicado, a única diferença para a função inicio() é que a variável contador é zerada, além de conter o <i>bind</i>.</li>
  <li>inicializar_coordenadas(event): o parâmetro <i>event</i> representa o evento, que no caso é o clique no canvas e as posições desse clique podem ser adquiridas por meio dos comandos: <i>event.x</i> e <i>event.y</i>. A variável contador tem um papel importante na determinação de qual condição de controle a posição do mouse será atribuída, são elas: ponto inicial, intermediário 1, intermediário 2 e ponto final. Após o contador ser maior do que 4 a função sai de sua recursividade, pois todas as condições de controle já foram adquiridas. 
  <li>imprimir_pontos(): apenas imprimi no canvas as condições de controle, monta uma lista de tuplas com todas as condições de controle e inicializa a função desenhar(points).</li>
</ul>
  
As funções responsáveis pela construção das curvas de Bezier foram adaptadas do algoritmo contido no link: https://github.com/NikolaiT/CunningCaptcha/blob/master/python_tests/casteljau.py. Essas funções são as seguintes:

<ul>
  <li>desenhar(points): inicializa o algoritmo que forma a curva de Bezier. O parâmetro "u" ,contido na função, é responável pela frequência em que se exibe os pixels intermediários e varia de 0 a 1 em 0,001. Quanto maior essa variação, por exemplo, em vez de 0.001 para 0.01, mais a linha da curva perde em continuidade, podendo se tornar uma linha pontilhada. Já o parâmetro recebido "points" é a lista de tuplas contendo todas as condições de controle.</li>
  <li>bezier(points, u): acrescenta novos pontos em um <i>array</i> chamado "novospontos" que são calculados de acordo com a equação de <i>Bernstein</i>. Essa equação leva em consideração o número de pontos de controle e o parâmetro "u". O número de pontos de controle vai diminuindo de um em um, até que se tenha apenas um, quando isso ocorre a função sai de sua recursividade e começa a preencher os pontos calculados pela equação de <i>Bernstein</i> por meio da função plot_pixel(x0,y0).</li>
  <li>plot_pixel(x0,y0): como o tkinter não possibilita o preenchimento de um pixel, essa função simula esse preenchimento imprimindo no canvas uma linha de 1cm na horizontal.</li>
</ul>

Quanto à estrutura de dados utilizada, os pontos são representados por dois inteiros, a posição x e a posição y. O método desenhar e bezier trabalham com uma lista desses pontos que são representados por tuplas com a posição x e y, ou seja, trabalham com uma lista de tuplas. O parâmetro "u" é um float, e o "contador" é um inteiro.

Link para download do algoritmo que inspirou as soluções implementadas para a montagem da curva de Bezier: https://github.com/NikolaiT/CunningCaptcha.

## Funcionamento da curva de Bezier

A curva de Bezier é uma curva que segue a forma do polígono de controle, estando dentro do seu fecho convexo. Esse polígono é  geralmente formado por quatro condições de controle, assim como mostra o exemplo abaixo, no qual os pontos destacados são as condições de controle.


Para um polígono de <i>n + 1</i> vértices, a curva de Bezier é uma curva paramétrica polinomial de grau <i>n</i> correspondente à fórmula abaixo, na qual ![bkn](https://user-images.githubusercontent.com/19623850/49144564-db450900-f2e4-11e8-87f8-d1721ba75526.gif) são <i>polinômios de Bernstein</i> e os vértices ![pk](https://user-images.githubusercontent.com/19623850/49145101-26135080-f2e6-11e8-9453-5b374c8ab212.gif)
 são os pesos, para que um vértice tenha mais peso e, consequentemente, a curva se aproxime dele, basta repetí-lo na equação.

![codecogseqn](https://user-images.githubusercontent.com/19623850/49144070-953b7580-f2e3-11e8-9068-6b606c03d107.gif?style=centerme)

Os <i>polinômios de Bernstein</i> possuem a seguinte fórmula:

![bernstein](https://user-images.githubusercontent.com/19623850/49145547-30821a00-f2e7-11e8-9b0c-76a89cd823f7.gif)

Nessa equação, o valor de <i>t</i> deve estar entre 0 e 1 para que a curva seja positiva. No algoritmo utilizado, o <i>t</i> é equivalente a variável "u", no qual quanto mais próxima de 0, mais a curva fica contínua. No código utilizado descrito abaixo é possível perceber como essa fórmula foi utilizada:

```
  def bezier(self, points, u):
    if (len(points) == 1):
      self.plot_pixel(points[0][0], points[0][1])
    else:
      novospontos = []
      for i in range(0, len(points)-1):
        x = (1-u) * points[i][0] + u * points[i+1][0]
        y = (1-u) * points[i][1] + u * points[i+1][1]
        novospontos.append((x, y))
      self.bezier(novospontos, u)
 ```

O "i", correspondente ao item da iteração, representa os vértices, condições de controle. Assim que se calcula para o "x" e o "y", a função é chamada recursivamente para os dois pontos. Essa parte correponte à combinação ![nk](https://user-images.githubusercontent.com/19623850/49147817-d7b58000-f2ec-11e8-86a7-0cb80503f7f8.gif) da fórmula de <i>Bernstein</i>. A lista de tuplas "points" contém os pontos referentes às condições de controle.


Referências: 
<ul>
  <li> http://www.mat.ufmg.br/~rodney/notas_de_aula/bezier.pdf </li>
  <li> http://www.portalsaberlivre.com.br/manager/uploads/educacional/1316553740.pdf </li>
</ul>

## Maneira de usar

Quando o programa se inicializa, uma janela com o título "Aplicação curva de Bezier" é aberta e nela contém a instrução "Escolha os quatro pontos de controle clicando na tela". Após clicar em quatro pontos da tela que serão os pontos de controle, é necessário clicar no botão "Montar a curva de Bezier" para montar a curva a partir desses pontos e, então, a curva é exibida. Também é exibido os pontos clicados, sendo os pontos iniciais e finais em vermelho, e os demais em azul. Para repetir o processo é necessário clicar no botão "Escolher novamente os pontos" e clicar na tela 4 vezes em 4 pontos diferentes e, então, apertar no botão "Montar a curva de Bezier" para que a curva seja montada. O processo pode ser repetido diversas vezes até que o usuário feche a aplicação. 

Para mais informações consultar o arquivo: Manual_do_usuario_beziercg.pdf.

Para ver o código funcionando, executar o vídeo Codigo_funcionando_beziercg.mp4.
