# Usar uma imagem base do Python
FROM python:3.9

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar os arquivos do projeto para o contêiner
COPY . .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir uvicorn

# Definir o comando para rodar a API
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5001"]

