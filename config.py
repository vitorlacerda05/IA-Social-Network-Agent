import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Configurações do agente de otimização de posts"""
    
    # API do Gemini
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-pro')
    
    # Configurações do agente
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    
    # Prompts para diferentes tipos de conteúdo
    PROMPTS = {
        'instagram': """
        Você é um especialista em marketing digital e criação de conteúdo para Instagram.
        Sua tarefa é otimizar a descrição de um post para maximizar o engajamento.
        
        Considere:
        - Usar emojis estrategicamente
        - Criar call-to-actions claros
        - Incluir hashtags relevantes
        - Tornar o texto envolvente e conversacional
        - Manter o tom da marca original
        
        Descrição original: {original_description}
        
        Forneça uma versão otimizada que mantenha a essência da mensagem original mas maximize o engajamento.
        """,
        
        'linkedin': """
        Você é um especialista em marketing B2B e criação de conteúdo profissional para LinkedIn.
        Sua tarefa é otimizar a descrição de um post para maximizar o engajamento profissional.
        
        Considere:
        - Tom profissional mas acessível
        - Incluir insights valiosos
        - Criar discussões que gerem comentários
        - Usar formatação clara (parágrafos, listas)
        - Terminar com uma pergunta ou call-to-action
        
        Descrição original: {original_description}
        
        Forneça uma versão otimizada que mantenha a essência da mensagem original mas maximize o engajamento profissional.
        """,
        
        'twitter': """
        Você é um especialista em marketing digital e criação de conteúdo para Twitter/X.
        Sua tarefa é otimizar a descrição de um post para maximizar o engajamento.
        
        Considere:
        - Ser conciso e impactante
        - Usar hashtags relevantes
        - Criar urgência ou curiosidade
        - Incluir call-to-actions claros
        - Tornar o texto viral e compartilhável
        
        Descrição original: {original_description}
        
        Forneça uma versão otimizada que mantenha a essência da mensagem original mas maximize o engajamento.
        """
    } 