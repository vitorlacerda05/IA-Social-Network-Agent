import streamlit as st
import json
from post_optimizer import PostOptimizer
from config import Config
import os

# Configuração da página
st.set_page_config(
    page_title="Agente de Otimização de Posts",
    page_icon="🚀",
    layout="wide"
)

# Título e descrição
st.title("🚀 Agente de Otimização de Posts")
st.markdown("""
Este agente usa IA para otimizar suas descrições de posts e maximizar o engajamento nas redes sociais.
""")

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Verificar se a API key está configurada
    if not Config.GEMINI_API_KEY:
        st.error("⚠️ Chave da API do Gemini não encontrada!")
        st.info("""
        Para usar este agente:
        
        1. Acesse: https://makersuite.google.com/app/apikey
        2. Crie uma chave API gratuita
        3. Crie um arquivo `.env` na raiz do projeto
        4. Adicione: `GEMINI_API_KEY=sua_chave_aqui`
        """)
        st.stop()
    
    # Seleção da plataforma
    platform = st.selectbox(
        "📱 Plataforma de destino",
        ["instagram", "linkedin", "twitter"],
        help="Selecione a rede social para otimizar o conteúdo"
    )
    
    # Configurações avançadas
    st.subheader("🔧 Configurações Avançadas")
    temperature = st.slider(
        "🎲 Criatividade",
        min_value=0.1,
        max_value=1.0,
        value=Config.TEMPERATURE,
        step=0.1,
        help="Valores mais altos geram conteúdo mais criativo"
    )
    
    max_tokens = st.slider(
        "📝 Tamanho máximo",
        min_value=100,
        max_value=2000,
        value=Config.MAX_TOKENS,
        step=100,
        help="Número máximo de caracteres na resposta"
    )

# Área principal
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Descrição Original")
    
    # Campo de texto para a descrição original
    original_description = st.text_area(
        "Cole sua descrição aqui:",
        height=200,
        placeholder="Ex: Hoje vou compartilhar algumas dicas sobre marketing digital..."
    )
    
    # Campo para contexto adicional
    additional_context = st.text_area(
        "Contexto adicional (opcional):",
        height=100,
        placeholder="Ex: Público-alvo: empreendedores, Objetivo: gerar leads..."
    )
    
    # Botão de otimização
    if st.button("🚀 Otimizar Post", type="primary", use_container_width=True):
        if original_description.strip():
            with st.spinner("Otimizando seu post..."):
                try:
                    # Inicializar o agente
                    optimizer = PostOptimizer()
                    
                    # Otimizar o post
                    result = optimizer.optimize_post(
                        original_description=original_description,
                        platform=platform,
                        additional_context=additional_context
                    )
                    
                    if result['success']:
                        st.session_state['result'] = result
                        st.success("✅ Post otimizado com sucesso!")
                    else:
                        st.error(f"❌ Erro: {result['error']}")
                        
                except Exception as e:
                    st.error(f"❌ Erro inesperado: {str(e)}")
        else:
            st.warning("⚠️ Por favor, insira uma descrição para otimizar.")

with col2:
    st.subheader("✨ Resultado Otimizado")
    
    if 'result' in st.session_state and st.session_state['result']['success']:
        result = st.session_state['result']
        
        # Exibir descrição otimizada
        st.text_area(
            "Descrição otimizada:",
            value=result['optimized_description'],
            height=200,
            key="optimized_output"
        )
        
        # Botões de ação
        col_copy, col_download = st.columns(2)
        
        with col_copy:
            if st.button("📋 Copiar", use_container_width=True):
                st.write("✅ Copiado para a área de transferência!")
                st.session_state['copied'] = True
        
        with col_download:
            # Preparar dados para download
            download_data = {
                'original': result['original_description'],
                'optimized': result['optimized_description'],
                'platform': result['platform'],
                'metrics': result['metrics'],
                'suggestions': result['suggestions']
            }
            
            st.download_button(
                label="💾 Baixar JSON",
                data=json.dumps(download_data, indent=2, ensure_ascii=False),
                file_name=f"post_otimizado_{platform}.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Métricas
        st.subheader("📊 Métricas")
        metrics = result['metrics']
        
        col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
        
        with col_metrics1:
            st.metric("📏 Tamanho", f"{metrics['optimized_length']} chars")
        
        with col_metrics2:
            st.metric("🏷️ Hashtags", metrics['hashtag_count'])
        
        with col_metrics3:
            st.metric("❓ Perguntas", metrics['question_count'])
        
        # Sugestões
        if result['suggestions']:
            st.subheader("💡 Sugestões")
            for suggestion in result['suggestions']:
                st.info(f"• {suggestion}")
    
    else:
        st.info("👈 Insira uma descrição e clique em 'Otimizar Post' para ver o resultado.")

# Seção de exemplos
with st.expander("📚 Exemplos de Uso"):
    st.markdown("""
    ### Exemplo 1 - Instagram
    **Original:** "Hoje vou falar sobre marketing digital"
    
    **Otimizado:** "🚀 Marketing Digital: O segredo do sucesso em 2024! 💡
    
    Quer saber como transformar seu negócio com estratégias digitais? 
    
    Neste post, vou compartilhar as técnicas que estão funcionando AGORA! 
    
    👇 Deixe nos comentários: qual é sua maior dificuldade com marketing digital?
    
    #MarketingDigital #Empreendedorismo #Negócios #Dicas #Sucesso"
    
    ### Exemplo 2 - LinkedIn
    **Original:** "A importância da liderança nas empresas"
    
    **Otimizado:** "A liderança não é apenas sobre dar ordens - é sobre inspirar pessoas a alcançarem seu potencial máximo.
    
    Durante minha jornada como executivo, aprendi que os melhores líderes:
    • Criam uma visão clara
    • Empoderam suas equipes
    • Lideram pelo exemplo
    • Focam no desenvolvimento contínuo
    
    Qual característica você considera mais importante em um líder? 
    
    Compartilhe sua experiência nos comentários! 👇"
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Desenvolvido com ❤️ usando Google Gemini API</p>
    <p>Para obter sua chave API gratuita: <a href='https://makersuite.google.com/app/apikey' target='_blank'>makersuite.google.com</a></p>
</div>
""", unsafe_allow_html=True) 