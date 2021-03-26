# CamadaFisicaProjeto2

Nesse projeto, utilizamos a base do projeto 1 (loopback) ṕara criar uma comunicaço entre arduinos (que representam 2 computadores distintos). Para isso, separamos a aplicacao.py do projeto 1 em aplicacaoServer.py e aplicacaoClient.py. O papel do client é enviar a imagem para o servidor (de acordo com as instruções do projeto), representando o tx. Já o Server, tem o papel de receber a imagem, copiá-la e devolver para o client essa cópia. Alguns dos detalhes que valem a pena citar são a necessidade de enviar bytes (hexadecimais) que representavam o tamanho da imagem antes de tudo, para que o server possa receber a imagem no seu tamanho verdadeiro. Assim como a necessidade de transformar esses bytes em números inteiros, para que o recebimento ocorra corretamente (já que o server não tem a imagem). Para maior eficiência, prints e variáveis antes utilizadas no projeto 1, mas sem uso nos códigos do projeto 2 foram removidas. Contudo, embora os prints sejam diversos e reduzem a velocide do processo, eles são muito úteis para a organizaço da aplicação.

Aqui está o link do vídeo que mostra o funcionamento do código sem a interação do usuário: 
https://drive.google.com/file/d/1_fjTibU-B256aVpIeVI3MO2gLq2AmvTj/view?usp=drivesdk

Este é o vídeo que mostra a interação do usuário com o input: 
Só o funcionamento (0:47): https://drive.google.com/file/d/1G_HWReCbBzOLTG7SmXaYF5RJtiTQOG7h/view?usp=drivesdk
Explicação + funcionamento (1:41): https://drive.google.com/file/d/1kfsAoZo_-DJQsfGofbRIIRVLrBRCzaXc/view?usp=drivesdk

(O primeiro é a parte essencial do segundo, caso não tenha tempo de ver tudo)
