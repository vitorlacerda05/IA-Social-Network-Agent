# 🚀 Agente de Otimização de Posts

Um agente inteligente que usa IA (Google Gemini) para otimizar descrições de posts e maximizar o engajamento nas redes sociais.

![image](https://github.com/user-attachments/assets/29d1b636-5531-4bba-9f14-24d856f811d9)

## ✨ Funcionalidades

- **Otimização Inteligente**: Usa IA para transformar descrições simples em posts envolventes
- **Múltiplas Plataformas**: Suporte para Instagram, LinkedIn e Twitter
- **Métricas Detalhadas**: Análise de hashtags, perguntas, exclamações e mais
- **Sugestões Personalizadas**: Dicas específicas para cada plataforma
- **Interface Web**: Interface amigável com Streamlit
- **CLI**: Interface de linha de comando para uso programático
- **Processamento em Lote**: Otimize múltiplos posts de uma vez

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd social-network-agent
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure a API do Gemini

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crie uma conta gratuita (se necessário)
3. Gere uma chave API gratuita
4. Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_api_aqui
GEMINI_MODEL=gemini-pro
```

## 🚀 Como Usar

### Interface Web (Recomendado)

Para rodar:
```bash
streamlit run app.py
```
Ou, diretamente pelo Python
```bash
python -m streamlit run app.py
```

Acesse `http://localhost:8501` no seu navegador.

### Linha de Comando

#### Otimizar um post individual:
```bash
python cli.py -d "Hoje vou falar sobre marketing digital" -p instagram
```

#### Com contexto adicional:
```bash
python cli.py -d "A importância da liderança" -p linkedin -c "Público: executivos, Objetivo: networking"
```

#### Processar múltiplos posts:
```bash
python cli.py -f posts.json -o resultados.json --pretty
```

### Uso Programático

```python
from post_optimizer import PostOptimizer

# Inicializar o agente
optimizer = PostOptimizer()

# Otimizar um post
result = optimizer.optimize_post(
    original_description="Hoje vou compartilhar dicas de marketing",
    platform="instagram",
    additional_context="Público: empreendedores"
)

if result['success']:
    print(f"Post otimizado: {result['optimized_description']}")
    print(f"Métricas: {result['metrics']}")
```

## 📊 Exemplos de Uso

### Exemplo 1: Instagram

**Entrada:**
```
"Hoje vou falar sobre marketing digital"
```

**Saída:**
```
🚀 Marketing Digital: O segredo do sucesso em 2024! 💡

Quer saber como transformar seu negócio com estratégias digitais? 

Neste post, vou compartilhar as técnicas que estão funcionando AGORA! 

👇 Deixe nos comentários: qual é sua maior dificuldade com marketing digital?

#MarketingDigital #Empreendedorismo #Negócios #Dicas #Sucesso
```

### Exemplo 2: LinkedIn

**Entrada:**
```
"A importância da liderança nas empresas"
```

**Saída:**
```
A liderança não é apenas sobre dar ordens - é sobre inspirar pessoas a alcançarem seu potencial máximo.

Durante minha jornada como executivo, aprendi que os melhores líderes:
• Criam uma visão clara
• Empoderam suas equipes
• Lideram pelo exemplo
• Focam no desenvolvimento contínuo

Qual característica você considera mais importante em um líder? 

Compartilhe sua experiência nos comentários! 👇
```

## 📁 Estrutura do Projeto

```
social-network-agent/
├── app.py              # Interface web com Streamlit
├── cli.py              # Interface de linha de comando
├── post_optimizer.py   # Classe principal do agente
├── config.py           # Configurações e prompts
├── requirements.txt    # Dependências Python
├── README.md          # Documentação
└── .env               # Variáveis de ambiente (criar)
```

## 🔧 Configurações

### Variáveis de Ambiente

- `GEMINI_API_KEY`: Sua chave API do Google Gemini
- `GEMINI_MODEL`: Modelo a ser usado (padrão: gemini-pro)

### Configurações do Agente

- `TEMPERATURE`: Criatividade da IA (0.1-1.0)
- `MAX_TOKENS`: Tamanho máximo da resposta
- `PROMPTS`: Prompts personalizados para cada plataforma

## 💡 Dicas de Uso

### Para Instagram:
- Use emojis estrategicamente
- Inclua hashtags relevantes
- Crie call-to-actions claros
- Faça perguntas para gerar comentários

### Para LinkedIn:
- Mantenha tom profissional
- Inclua insights valiosos
- Use formatação clara
- Termine com perguntas para discussão

### Para Twitter:
- Seja conciso e impactante
- Use hashtags relevantes
- Crie urgência ou curiosidade
- Torne o conteúdo viral

## 🆓 Gratuito e Sem Limites

- **API Gratuita**: Google Gemini oferece tier gratuito generoso
- **Sem Limites**: Use quantas vezes quiser
- **Sem Cadastro**: Apenas a chave API é necessária

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request


## 🆘 Suporte

Se encontrar algum problema:

1. Verifique se a chave API está configurada corretamente
2. Confirme se todas as dependências estão instaladas
3. Verifique a documentação da API do Gemini
4. Abra uma issue no GitHub

## 🔗 Links Úteis

- [Google AI Studio](https://makersuite.google.com/app/apikey) - Obter chave API
- [Documentação Gemini](https://ai.google.dev/docs) - Documentação oficial
- [Streamlit](https://streamlit.io/) - Framework da interface web 
