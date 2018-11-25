#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Trabalho de Computacao Grafica: curvas 
Aluna: Giovanna Avila Riqueti
Codigo de inspiracao: https://github.com/NikolaiT/CunningCaptcha/blob/master/python_tests/casteljau.py
"""

from tkinter import *
from matplotlib import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from scipy import special


class CurvaBezier:

	def __init__(self, master=None):
		self.widget1 = Frame(master)
		self.widget1.pack()
		self.fontePadrao = ("Arial", "10")

		self.canvas_width = 800
		self.canvas_height = 500

		self.primeiroContainer = Frame(master)
		self.primeiroContainer["padx"] = 10
		self.primeiroContainer.pack()

		self.segundoContainer = Frame(master)
		self.segundoContainer["padx"] = 10
		self.segundoContainer.pack()

		self.w = Canvas(self.segundoContainer,
		   width=self.canvas_width,
		   height=self.canvas_height)
		self.w.pack(expand=YES, fill=BOTH)

		#Mensagem informando instrucao para comecar
		self.label1 = Label(self.primeiroContainer,text=u"Escolha os quatro pontos de controle clicando na tela.", font=self.fontePadrao)
		self.label1.pack()

		#primeira coordenada
		self.xinicial = -1
		self.yinicial = -1

		#segunda coordenada
		self.x1 = -1
		self.y1 = -1

		#terceira coordenada
		self.x2 = -1
		self.y2 = -1

		#quarta coordenada
		self.xfinal = -1
		self.yfinal = -1

		#Contador para que sejam escolhidas somente 4 posicoes, condicoes de controle
		self.contador = 0

		#Botao para montar a curva
		self.botaoCurvaInicial = Button(self.primeiroContainer)
		self.botaoCurvaInicial["font"] = self.fontePadrao
		self.botaoCurvaInicial["width"] = 25
		self.botaoCurvaInicial["text"] = 'Montar a curva de Bezier'
		self.botaoCurvaInicial["command"] = self.imprimir_pontos
		self.botaoCurvaInicial.pack(side=LEFT)
		
		#Chamada da funcao inicio() assim que a aplicacao se inicializa
		self.inicio()

		#Botao para escolher os pontos novamente
		self.botaoEscolher = Button(self.primeiroContainer)
		self.botaoEscolher["font"] = self.fontePadrao
		self.botaoEscolher["width"] = 25
		self.botaoEscolher["text"] = 'Escolher novamente os pontos'
		self.botaoEscolher["command"] = self.inicio2
		self.botaoEscolher.pack(side=LEFT)


	#Funcao que se inicia quando o programa se inicia
	def inicio(self):
		self.w.bind("<Button 1>", self.inicializar_coordenadas)

	#Funcao que se inicia quando o quando o botao: "botaoescolher" e' apertado
	def inicio2(self):
		self.contador = 0
		self.w.bind("<Button 2>", self.inicializar_coordenadas)
		

	#Metodo para pegar as coordenadas de onde o mouse clicou e a atribuir ao valor da variavel correta
	def inicializar_coordenadas(self, event):
		if (self.contador == 0):
			self.xinicial = event.x
			self.yinicial = event.y
			
		elif (self.contador == 1):
			self.x1 = event.x
			self.y1 = event.y

		elif (self.contador == 2):
			self.x2 = event.x
			self.y2 = event.y
			
		elif (self.contador == 3):
			self.xfinal = event.x
			self.yfinal = event.y
			
		self.contador += 1
		#Verificar se todas as posicoes foram preenchidas, caso nao forem a funcao e' chamada novamente
		if (self.contador < 4):
			self.w.bind("<Button 1>", self.inicializar_coordenadas)




	def imprimir_pontos(self):
		#Printar as coordenadas, sendo os pontos iniciais e finais em vermelho
		self.w.create_text(self.xinicial, self.yinicial, text = "o", tag = "line", fill='#ff1a1a', width=999)
		self.w.create_text(self.x1, self.y1, text = "o", tag = "line", fill="#4d4dff", width=999)
		self.w.create_text(self.x2, self.y2, text = "o", tag = "line", fill="#4d4dff", width=999)
		self.w.create_text(self.xfinal, self.yfinal, text = "o", tag = "line", fill='#ff1a1a', width=999)
		#Criando lista de pontos para serem usados no algoritmo
		points = [(int(self.xinicial), int(self.yinicial)), (int(self.x1), int(self.y1)), (int(self.x2), int(self.y2)), (int(self.xfinal), int(self.yfinal))]
		self.desenhar(points)


		
	#Inicializa o algoritmo que forma a curva se Bezier
	def desenhar(self, points):
		#A variavel "u" representa o parametro levado em consideracao para o calculo das posicoes intermediarias
		#"u" varia de 0 a 1 em 0.001
		u = 0
		while (u <= 1):
			self.bezier(points, u)
			u += 0.001


	def bezier(self, points, u):
		if (len(points) == 1):
			#Somente constroi uma linha, simulando o tamanho do pixel
			self.plot_pixel(points[0][0], points[0][1])
		else:
			#Calculo dos pontos intermediarios
			#Utiliza-se a equacao de Bernstein para a construcao dos pontos intermediarios das curvas
			novospontos = []
			for i in range(0, len(points)-1):
				x = (1-u) * points[i][0] + u * points[i+1][0]
				y = (1-u) * points[i][1] + u * points[i+1][1]
				novospontos.append((x, y))
			#Chamada recursiva que termina apenas quando novospontos possuir tamanho 1 ou seja, ter apenas uma posicao, pois as outras ja' foram calculadas
			self.bezier(novospontos, u)



	def plot_pixel(self, x0, y0):
		#E' construido uma linha de 1cm na horizontal para simular um pixel
		self.w.create_line(x0, y0, x0+1, y0)


#Inicializacao do Tkinter e da aplicacao
root1 = Tk()
app = CurvaBezier(root1)
root1.title(u"Aplicação curva de Bezier.")
root1.mainloop()

