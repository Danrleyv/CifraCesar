import cv2

#Função do Professor para decriptografar a imagem
def decriptografar(img):
    imgDec = (img % 4) * 64
    return imgDec

#Função para criar uma matriz de qualquer tamanho inicializada com 0
def criaMatriz(n_linhas, n_colunas):
    matriz = []  # lista vazia
    for i in range(n_linhas):
        # cria a linha i
        linha = []  # lista vazia
        for j in range(n_colunas):
            linha.append(0)

        # coloque linha na matriz
        matriz.append(linha)

    return matriz

#Função que transforma um numero decimal de 0 a 255 em um array de 8 bits
def toBinary(num):
    bitString = [0, 0, 0, 0, 0, 0, 0, 0]

    #Armazena na ordem binaria da direita para a esquerda
    pos = 7
    while (num > 0):
        if ((num % 2) == 1):
            bitString[pos] = 1
            num = num - 1
            num = num / 2
        else:
            bitString[pos] = 0
            num = num / 2

        pos = pos - 1

    return bitString

#Função que transforma um array de 8 bits em um numero decimal de 0 a 255
def toDecimal(bitString):
    num = 0

    pos = 7
    x = 0
    while (pos >= 0):
        num = num + (bitString[pos] * (2 ** x))
        pos = pos - 1
        x = x + 1

    return num

#Função que realiza a esteganografia de imagens
#Recebe a imagem a ser escondida (img1) e a imagem a ser transformada (img2)
def esteganografia(img1, img2):
    #Cria uma matriz para cada canal de cor da imagem 1
    bitArrayB1 = criaMatriz(512, 512)
    bitArrayG1 = criaMatriz(512, 512)
    bitArrayR1 = criaMatriz(512, 512)

    #Cria uma matriz para cada canal de cor da imagem 2
    bitArrayB2 = criaMatriz(512, 512)
    bitArrayG2 = criaMatriz(512, 512)
    bitArrayR2 = criaMatriz(512, 512)
    #Tamanho 512 pois é o tamanho da imagem

    #Loop que trasforma cada cor de cada pixel das duas imagens em um array de 8 bits
    i = 0
    while (i < 512):
        j = 0
        while (j < 512):
            bitArrayB1[i][j] = toBinary(img1[i][j][0])
            bitArrayG1[i][j] = toBinary(img1[i][j][1])
            bitArrayR1[i][j] = toBinary(img1[i][j][2])

            bitArrayB2[i][j] = toBinary(img2[i][j][0])
            bitArrayG2[i][j] = toBinary(img2[i][j][1])
            bitArrayR2[i][j] = toBinary(img2[i][j][2])

            j = j + 1

        i = i + 1

    #Loop que realiza a alocação dos dois bits mais relevantes da imagem 1
    #para os dois menos relevantes da imagem 2
    i = 0
    while (i < 512):
        j = 0
        while (j < 512):
            bitArrayB2[i][j][6] = bitArrayB1[i][j][0]
            bitArrayB2[i][j][7] = bitArrayB1[i][j][1]

            bitArrayG2[i][j][6] = bitArrayG1[i][j][0]
            bitArrayG2[i][j][7] = bitArrayG1[i][j][1]

            bitArrayR2[i][j][6] = bitArrayR1[i][j][0]
            bitArrayR2[i][j][7] = bitArrayR1[i][j][1]

            j = j + 1

        i = i + 1

    #Loop que trasforma cada array com a cor alterada novamente na imagem 2
    i = 0
    while (i < 512):
        j = 0
        while (j < 512):
            img2[i][j][0] = toDecimal(bitArrayB2[i][j])
            img2[i][j][1] = toDecimal(bitArrayG2[i][j])
            img2[i][j][2] = toDecimal(bitArrayR2[i][j])

            j = j + 1

        i = i + 1

    #Retorna a imagem alterada
    return img2


img1 = cv2.imread("lenna.png")
img2 = cv2.imread("paisagem.png")

#cv2.imshow("Lenna", img1)
#cv2.imshow("Pasagem", img2)
#cv2.waitKey(0)

#Armazena a imagem alterada
imgfinal = esteganografia(img1, img2)

#Decriptografa para confirmar que funcionou
cv2.imshow("Final", imgfinal)
cv2.imshow("Final Decriptografada", decriptografar(imgfinal))
cv2.waitKey(0)