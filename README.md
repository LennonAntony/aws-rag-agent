🚀 Guia de Deploy – AWS RAG Agent (EC2 + Milvus + OpenAI + S3)

Este guia explica como configurar e executar um sistema de RAG (Retrieval-Augmented Generation) utilizando:

AWS EC2

Docker

Milvus

OpenAI API

Amazon S3

FastAPI

🖥️ Criar Instância EC2

Crie uma instância EC2 com:

Sistema Operacional: Ubuntu 22.04 LTS (64-bit x86)

Tipo: t3.micro (ou superior)

Armazenamento: 30GB gp3

Key pair: RSA (.pem)

⚠️ Nunca exponha seu IP público ou sua chave privada.

🔐 Conectar via SSH
ssh -i sua_key.pem ubuntu@SEU_IP_PUBLICO

🐳 Instalar Docker e Dependências
sudo apt update
sudo apt upgrade -y
sudo apt install docker.io docker-compose python3-pip -y
sudo systemctl enable docker
sudo usermod -aG docker ubuntu


Saia e conecte novamente.

Teste:

docker ps

📦 Subir Milvus com Docker
curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh | bash -s start


Verifique:

docker ps


O Milvus deve estar rodando na porta 19530.

🔓 Configurar Security Group

Adicionar regras de entrada:

Tipo	Porta	Origem
Custom TCP	19530	0.0.0.0/0
Custom TCP	8000	0.0.0.0/0

⚠️ Em produção, restrinja os IPs.

🐍 Configurar Ambiente Python
mkdir rag-agent
cd rag-agent
sudo apt install python3.12-venv -y
python3 -m venv venv
source venv/bin/activate


Instalar dependências:

pip install -r requirements.txt

📥 Clonar Projeto do GitHub
git clone https://github.com/LennonAntony/aws-rag-agent.git
cd aws-rag-agent


Estrutura do projeto:

main.py

search.py

ingest.py

embeddings.py

llm.py

vector_store.py

create_collection.py

🔑 Configurar Variáveis de Ambiente

Criar arquivo .env:

nano .env


Adicionar:

OPENAI_API_KEY=sua_chave_aqui


⚠️ Nunca publique esse arquivo no GitHub.

🗂️ Criar Collection no Milvus
python create_collection.py

☁️ Criar Bucket no S3

Crie um bucket, por exemplo:

rag-agent-documents


Faça upload dos PDFs para teste.

🔐 Associar Role IAM à EC2

Criar Role:

Serviço: EC2

Permissão: AmazonS3ReadOnlyAccess

Associar essa role à instância EC2.

📡 Instalar AWS CLI
sudo apt install unzip curl -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install


Testar:

aws --version
aws s3 ls

📄 Rodar Ingestão de Documentos
python ingest.py


Isso irá:

Ler PDFs do S3

Gerar embeddings

Inserir vetores no Milvus

🚀 Iniciar Servidor FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000


Acessar:

http://SEU_IP_PUBLICO:8000/docs

🧠 Fluxo do Sistema

PDF armazenado no S3

Extração de texto

Divisão em chunks

Geração de embeddings

Armazenamento no Milvus

Usuário envia pergunta

Busca por similaridade

OpenAI gera resposta final
